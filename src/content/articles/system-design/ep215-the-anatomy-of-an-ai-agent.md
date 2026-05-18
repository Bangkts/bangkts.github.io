---
title: "EP215: The Anatomy of an AI Agent"
category: "System Design"
categoryOrder: 1
order: 4
source: "https://blog.bytebytego.com/p/ep215-the-anatomy-of-an-ai-agent"
sourceLabel: "ByteByteGo"
---

## Tiêm nhanh chóng, giải thích rõ ràng

[Video 1](https://www.youtube.com/watch?v=KDcayRssGbw)

## Giải phẫu của một đặc vụ AI

Một tác nhân AI có thể được coi như một vòng lặp while đơn giản.

[![Hình 5: Hình ảnh](__IMGURL_0__)](https://substackcdn.com/image/fetch/$s_!lOfS!,f_auto,q_auto:good,fl_progressive:steep/https% 3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20aada1f-cc38-4c94-8778-eeaa7b63aceb_2484x3002.png)

Nó sử dụng LLM để chọn một hành động, thực hiện hành động đó, đánh giá kết quả và lặp lại quy trình cho đến khi nhiệm vụ hoàn thành. Chúng ta hãy xem xét kỹ hơn từng thành phần này:

*   Não: LLM là cốt lõi. Nó đọc tình huống, suy nghĩ và quyết định phải làm gì tiếp theo. Sự thay đổi lớn từ chatbot sang tổng đài viên: mô hình không viết văn bản nữa mà đưa ra lựa chọn.

*   Lập kế hoạch: Những nhiệm vụ khó khăn cần nhiều hơn một bước. Đại lý chia nhỏ chúng bằng các phương pháp như Chuỗi suy nghĩ (suy nghĩ từng bước), Cây suy nghĩ (thử các phương án, chọn phương án tốt nhất) hoặc

Phản xạ (rút kinh nghiệm từ sai lầm và thử lại). Lập kế hoạch biến mục tiêu mơ hồ thành hành động rõ ràng.

*   Công cụ: LLM không có công cụ giống như một bộ não trong lọ. Công cụ là các chức năng mà mô hình có thể gọi, như tìm kiếm trên web, thực thi mã, API, tệp hoặc trình duyệt (thường sử dụng tiêu chuẩn MCP). Mô hình yêu cầu một công cụ, hệ thống chạy nó và trả về kết quả.

*   Bộ nhớ: Không có bộ nhớ, mỗi lượt đều bắt đầu từ số 0. Bộ nhớ ngắn hạn là cửa sổ ngữ cảnh. Trí nhớ dài hạn tồn tại trong các kho lưu trữ vector, tệp và cơ sở kiến ​​thức. Khi cửa sổ đầy, các đặc vụ tóm tắt các lượt cũ và chuyển bản tóm tắt về phía trước.

*   Vòng lặp: Tất cả bốn phần hoạt động cùng nhau trong một chu trình. Tác nhân xem xét trạng thái hiện tại, quyết định phải làm gì, sử dụng công cụ, xem kết quả và lặp lại. Nó tiếp tục cho đến khi nó đưa ra câu trả lời cuối cùng.

*   Lan can: Không hẳn là giải phẫu, nhưng quan trọng. Hộp cát, kiểm tra của con người, giới hạn mã thông báo, xác thực đầu ra và giới hạn phạm vi giúp quyền tự chủ không trở thành sự hỗn loạn tốn kém. Bạn càng trao nhiều quyền tự chủ thì những vấn đề này càng trở nên quan trọng hơn.

Gửi đến bạn: khi bạn xây dựng một đại lý, điều nào trong số năm điều này sẽ tốn nhiều công sức nhất để đạt được đúng?

## REST so với GraphQL so với gRPC

REST, GraphQL và gRPC là ba cách tiếp cận riêng biệt để thiết kế API. Mỗi loại cung cấp một sự đánh đổi khác nhau giữa tính đơn giản, hiệu suất và tính linh hoạt.

[![Hình 6: Hình ảnh](__IMGURL_1__)](https://substackcdn.com/image/fetch/$s_!eDv8!,f_auto,q_auto:good,fl_progressive:steep/https% 3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffafb183d-5c2f-4a6e-994e-ecba33663b11_2484x3002.png)

1.   REST: Mỗi URL đại diện cho một tài nguyên và bạn sử dụng các động từ HTTP tiêu chuẩn (GET, POST, PUT, DELETE) để hành động trên đó. Đơn giản và phổ quát nhưng thường đòi hỏi nhiều yêu cầu để tập hợp dữ liệu liên quan.

Đánh đổi: Dễ học, thân thiện với bộ đệm và hoạt động với bất kỳ ứng dụng khách HTTP nào, nhưng có xu hướng tìm nạp quá mức hoặc tìm nạp dữ liệu dưới mức, dẫn đến các ứng dụng khách trò chuyện và phiên bản bị trôi khi điểm cuối tăng sinh.

2.   GraphQL: Máy khách gửi truy vấn mô tả chính xác hình dạng dữ liệu cần thiết và máy chủ trả về chính xác dữ liệu đó thông qua một điểm cuối duy nhất.

Đánh đổi: Loại bỏ việc tìm nạp quá mức và cho phép các giao diện người dùng phát triển độc lập nhưng chuyển độ phức tạp sang máy chủ (bộ phân giải, truy vấn N+1), làm phức tạp bộ nhớ đệm và khiến việc giới hạn tốc độ cũng như phân tích chi phí truy vấn trở nên khó khăn hơn.

3.   gRPC: Các dịch vụ giao tiếp thông qua các cuộc gọi phương thức được gõ mạnh qua HTTP/2 bằng cách sử dụng mã hóa nhị phân (protobuf) nhỏ gọn, lý tưởng cho việc liên lạc giữa các dịch vụ với dịch vụ nhanh chóng, có độ trễ thấp với tính năng hỗ trợ phát trực tuyến tích hợp.

Đánh đổi: Hiệu suất tuyệt vời và các hợp đồng nghiêm ngặt thông qua lược đồ protobuf, nhưng định dạng nhị phân không thể đọc được, hỗ trợ trình duyệt yêu cầu proxy (gRPC-Web) và việc gỡ lỗi khó hơn so với JSON đơn giản qua HTTP.

Nguyên tắc chung: REST dành cho các API công khai và khả năng tương thích rộng, GraphQL khi khách hàng cần chế độ xem tổng hợp, linh hoạt và gRPC cho các dịch vụ vi mô nội bộ nơi độ trễ và thông lượng quan trọng nhất.

## Nếu Claude Code là một chiếc burger...

Trước mỗi lệnh gọi mô hình, Claude Code tập hợp một cửa sổ ngữ cảnh từ 9 nguồn riêng biệt.

Hãy coi nó như một chiếc bánh mì kẹp thịt, mỗi lớp sẽ thêm một thứ gì đó khác nhau.

[![Hình 7: Hình ảnh](__IMGURL_2__)](https://substackcdn.com/image/fetch/$s_!N0Ju!,f_auto,q_auto:good,fl_progressive:steep/https%3 A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae110097-f828-4b76-ba3c-de2a774a4ea7_2484x3002.jpeg)

1.   Lời nhắc hệ thống: Xác định vai trò, hành vi và giọng điệu của Claude. Điều này đặt nền tảng.

2.   Thông tin môi trường: Trạng thái Git, thông tin chi nhánh và ngày hiện tại. Được kéo qua getSystemContext()

3.   CLAUDE. md: Hệ thống phân cấp hướng dẫn bốn cấp: được quản lý → người dùng → dự án → cục bộ. Đánh dấu văn bản thuần túy để người dùng có thể đọc, chỉnh sửa và kiểm soát phiên bản mọi thứ mà mô hình nhìn thấy.

4.   Bộ nhớ tự động: Các mục nhập bộ nhớ có liên quan theo ngữ cảnh được tìm nạp trước không đồng bộ. LLM quét các tiêu đề tệp bộ nhớ và hiển thị tối đa 5 tệp có liên quan theo yêu cầu.

5.   Quy tắc trong phạm vi đường dẫn: Quy tắc có điều kiện tải chậm khi tác nhân đọc tệp

6.   Siêu dữ liệu công cụ: Mô tả kỹ năng, tên công cụ MCP và định nghĩa công cụ trì hoãn.

7.   Lịch sử hội thoại: Được chuyển tiếp qua các lần lặp lại.

8.   Kết quả công cụ: Đọc tệp, xuất lệnh và tóm tắt tác nhân phụ.

9.   Tóm tắt ngắn gọn: Khi lịch sử phát triển quá dài, các phân đoạn cũ hơn sẽ được thay thế bằng các tóm tắt do mô hình tạo.

Toàn bộ thiết kế coi bối cảnh như một nguồn tài nguyên khan hiếm.

Gửi bạn: Bạn điều chỉnh lớp nào trong 9 lớp này nhiều nhất khi làm việc với Claude Code?

## git tìm nạp vs git pull vs git pull —rebase

Hầu hết các lỗi Git không đến từ một cam kết xấu. Chi nhánh của bạn ở phía sau, bạn có các cam kết cục bộ và bây giờ bạn cần thực hiện các thay đổi ngược dòng. Đó là lúc sự khác biệt giữa gitfetch, git pull và git pull —rebase trở nên quan trọng.

[![Hình 8: Hình ảnh](__IMGURL_3__)](https://substackcdn.com/image/fetch/$s_!71ii!,f_auto,q_auto:good,fl_progressive:steep/https% 3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68416644-193b-4b64-8e50-2e36a950b890_2484x3002.png)

git get tải xuống các thay đổi và cập nhật từ xa Origin/main. Chính địa phương của bạn không di chuyển. Không có gì trong thư mục làm việc của bạn thay đổi. Điều đó làm cho việc tìm nạp trở thành tùy chọn an toàn nhất khi bạn muốn kiểm tra những gì đã thay đổi ở thượng nguồn trước khi tích hợp bất kỳ thứ gì.

git pull tiến thêm một bước nữa. Nó tìm nạp trước rồi hợp nhất nhánh ngược dòng vào nhánh hiện tại của bạn. Các cam kết cục bộ của bạn vẫn được giữ nguyên và Git thêm một cam kết hợp nhất để kết nối hai lịch sử.

git pull —rebase là thứ sạch sẽ. Nó bắt đầu bằng việc tìm nạp, nhưng thay vì hợp nhất, nó sẽ áp dụng lại các cam kết cục bộ của bạn trên nhánh thượng nguồn đã cập nhật. Kết quả là một lịch sử tuyến tính không có cam kết hợp nhất.

Tìm nạp khi bạn chỉ muốn xem những gì trên điều khiển từ xa trước khi quyết định bất cứ điều gì. Kéo khi bạn đang ở trên chi nhánh của riêng mình và không bận tâm đến các cam kết hợp nhất hiển thị trong nhật ký. Rebase khi bạn đang dọn dẹp một nhánh tính năng trước khi mở PR và muốn lịch sử được đọc rõ ràng.

Gửi cho bạn: Làm thế nào để bạn xử lý một nhánh tính năng đã tồn tại được vài ngày trong khi nhánh chính đã di chuyển trước 10 lần xác nhận?
