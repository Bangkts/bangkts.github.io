---
title: "How Grab is Using AI Agents to Boost Team Productivity"
category: "System Design"
categoryOrder: 1
order: 5
source: "https://blog.bytebytego.com/p/how-grab-is-using-ai-agents-to-boost"
sourceLabel: "ByteByteGo"
---

Nhóm kỹ thuật dữ liệu của Grab gặp phải một vấn đề quen thuộc với bất kỳ ai duy trì cơ sở hạ tầng dùng chung. Những kỹ sư giỏi nhất của họ đã dành trọn hai ngày mỗi tuần để trả lời những câu hỏi nhanh từ đồng nghiệp.

Để tham khảo, Grab là một siêu ứng dụng trên khắp Đông Nam Á xử lý các chuyến đi, giao đồ ăn, thanh toán, v.v. Tất cả hoạt động đó tạo ra lượng dữ liệu khổng lồ và nhóm Kho dữ liệu phân tích (ADW) chịu trách nhiệm tổ chức và cung cấp dữ liệu đó cho các bộ phận còn lại của công ty.

Nhóm này quản lý hơn 15.000 bảng, cung cấp gần một nửa tổng số truy vấn trong hồ dữ liệu của Grab và khoảng 1.000 người trên toàn công ty truy vấn các bảng đó mỗi tháng. Các nhà phân tích, giám đốc sản phẩm và các kỹ sư khác đều phụ thuộc vào bảng của nhóm ADW để thực hiện công việc của họ.

Điều đó khiến nhóm ADW trở thành thủ thư quản lý dữ liệu của Grab, đồng thời cũng là bộ phận trợ giúp. Các câu hỏi được đặt ra rất nhanh, chẳng hạn như "Tại sao ID này trông giống như vô nghĩa?" hoặc “Bạn có thể thêm một cột vào bảng này không?”

Tuy nhiên, mỗi câu trả lời đều yêu cầu một hành trình phân mảnh thông qua các danh mục dữ liệu, truy tìm dòng dõi thủ công, xác thực SQL và tìm hiểu nhật ký. Vì vậy họ đã xây dựng một hệ thống AI đa tác nhân để tự động hóa quá trình điều tra. Hệ thống hoạt động rất tốt trong các bản demo. Sau đó, họ chuyển nó đi sản xuất và có sáu thứ bị hỏng.

Nhưng trước khi tìm hiểu những gì đã xảy ra và cách nhóm xử lý mọi việc, hãy cùng chúng tôi hiểu những gì họ đã xây dựng.

_Tuyên bố từ chối trách nhiệm: Bài đăng này dựa trên thông tin chi tiết được chia sẻ công khai từ Nhóm Kỹ thuật Grab. Hãy bình luận nếu bạn nhận thấy bất kỳ sự không chính xác._

## Mô hình đằng sau vấn đề

Nhóm ADW đã theo dõi cấu trúc của những câu hỏi này và nhận thấy một điều quan trọng. Mặc dù mỗi câu hỏi đều khác nhau nhưng quá trình trả lời chúng khá nhất quán. Một kỹ sư sẽ tìm kiếm thông qua các danh mục dữ liệu, theo dõi dữ liệu đến từ đâu, xác thực nó bằng các truy vấn SQL và kiểm tra nhật ký quy trình. Các câu hỏi rất đa dạng, nhưng cẩm nang điều tra vẫn giữ nguyên. Sự nhất quán này là tín hiệu cho một cơ hội tự động hóa có thể xảy ra.

Triết lý thiết kế của họ bắt đầu bằng sự tách biệt rõ ràng mà họ mô tả là tách rời bộ não khỏi bàn tay.

Bộ não là LLM thực hiện việc lý luận. Bàn tay là tác nhân và công cụ chuyên dụng thực sự lấy thông tin, chạy truy vấn và tương tác với hệ thống. Bằng cách tách biệt hai mối quan tâm này, họ đã tạo ra một hệ thống vừa có khả năng vừa dễ gỡ lỗi. Khi có sự cố xảy ra, họ có thể xác định xem vấn đề là do lý do hay do tương tác công cụ cụ thể.

Họ cũng đã cố tình đặt cược vào kiến ​​trúc.

Thay vì xây dựng một AI khổng lồ được đào tạo để xử lý mọi loại câu hỏi, họ đã xây dựng nhiều tác nhân chuyên biệt, mỗi tác nhân tập trung vào một miền hẹp.

Xem sơ đồ bên dưới để biết cách hoạt động của tác nhân AI:

[![Image 5](https://substackcdn.com/image/fetch/$s_!w053!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a3f60c2-0a22-4f92-a2c3-20162ce0bf14_2114x1374.png)](https://substackcdn.com/image/fetch/$s_!w053!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a3f60c2-0a22-4f92-a2c3-20162ce0bf14_2114x1374.png)

Một mô hình nguyên khối duy nhất sẽ dễ triển khai hơn với một mô hình và một lệnh gọi suy luận, nhưng cũng sẽ khó gỡ lỗi hơn và bất kỳ thay đổi nào cũng có nguy cơ ảnh hưởng đến mọi thứ. Mặt khác, các tác nhân chuyên biệt có tính mô-đun. Bạn có thể cải thiện một cái mà không cần chạm vào những cái khác, thêm cái mới mà không cần viết lại hệ thống và phân công trách nhiệm rõ ràng để giúp theo dõi các lỗi có thể xảy ra. Sự cân bằng là độ phức tạp của việc phối hợp và một số độ trễ được thêm vào do thực hiện tuần tự.

Hãy xem sự so sánh dưới đây:

[![Image 6](https://substackcdn.com/image/fetch/$s_!0Hdw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F453b9b03-616d-46f2-a0fa-229090a6f691_3164x1526.png)](https://substackcdn.com/image/fetch/$s_!0Hdw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F453b9b03-616d-46f2-a0fa-229090a6f691_3164x1526.png)

Grab chấp nhận sự đánh đổi đó vì khả năng bảo trì và độ chính xác quan trọng hơn việc tiết kiệm được vài giây. Ý tưởng là khi bạn thay thế việc điều tra thủ công kéo dài nhiều giờ, thì một vài phút để có câu trả lời chính xác là một cải tiến lớn.

Về mặt công nghệ, họ đã sử dụng FastAPI để xử lý các yêu cầu đến và LangGraph để quản lý logic trạng thái phức tạp mà hoạt động cộng tác giữa nhiều tác nhân yêu cầu. Các cuộc gọi LLM đơn giản diễn ra theo một đường thẳng từ đầu vào đến đầu ra, nhưng các đại lý của Grab cần quay lại, hỏi thêm thông tin hoặc giao nhiệm vụ cho nhau và LangGraph hỗ trợ loại quy trình làm việc theo chu kỳ đó. Redis xử lý các nhu cầu về bộ nhớ đệm và phiên thời gian thực, trong khi PostgreSQL lưu trữ lịch sử hội thoại và siêu dữ liệu tác nhân dưới dạng bộ nhớ liên tục. Bản thân các đại lý lấy thông tin từ ba nền tảng nội bộ, như sau:

*   Hubble phục vụ như một danh mục dữ liệu và siêu dữ liệu tập trung.

*   Genchi là một nền tảng quan sát chất lượng dữ liệu nhằm thực thi các hợp đồng dữ liệu.

*   Lighthouse theo dõi trạng thái và tình trạng thực hiện đường ống.

Xem sơ đồ dưới đây:

[![Image 7](https://substackcdn.com/image/fetch/$s_!d-Di!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b57642c-036d-484c-b36f-ef1aed886767_2232x2304.png)](https://substackcdn.com/image/fetch/$s_!d-Di!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b57642c-036d-484c-b36f-ef1aed886767_2232x2304.png)

**Nguồn:**[Blog Kỹ thuật Grab](https://engineering.grab.com/from-firefighting-to-building)

Với kiến ​​trúc đã có, quyết định thiết kế tiếp theo là làm thế nào để phân chia công việc. Sự phân chia này hóa ra là một trong những lựa chọn quan trọng nhất trong toàn bộ hệ thống.

## Hai Con đường, Năm Agents, Một Người giám sát

Khi có câu hỏi được gửi qua Slack, trước tiên, hệ thống sẽ xác định con đường nào trong hai con đường sẽ thực hiện. Ngã ba này là xương sống kiến ​​trúc của toàn bộ hệ thống và nó dựa trên một nguyên tắc quan trọng. Hoạt động chỉ đọc và hoạt động ghi có hồ sơ rủi ro khác nhau về cơ bản, vì vậy chúng xứng đáng có các kiến ​​trúc cơ bản khác nhau.

Xem sơ đồ dưới đây:

[![Image 8](https://substackcdn.com/image/fetch/$s_!J_Fv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b1896cf-0b6b-46d0-9b7b-0654a1464e59_1752x2346.png)](https://substackcdn.com/image/fetch/$s_!J_Fv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b1896cf-0b6b-46d0-9b7b-0654a1464e59_1752x2346.png)

**Nguồn:**[Blog Kỹ thuật Grab](https://engineering.grab.com/from-firefighting-to-building)

Lộ trình điều tra xử lý các câu hỏi như "Tại sao dữ liệu này có vẻ sai?" hoặc “Số liệu này đến từ đâu?” Đây là những chỉ đọc. Hệ thống đang thu thập thông tin và trường hợp xấu nhất là một câu trả lời sai sẽ bị đưa vào xem xét. Bốn đại lý hợp tác ở đây như sau:

*   Trình phân loại là phản hồi đầu tiên. Nó phân tích câu hỏi, trích xuất các thực thể chính như tên bảng và tham chiếu cột, phát hiện các vi phạm lan can như yêu cầu PII hoặc truy vấn ngoài phạm vi, đồng thời xác định cần có tác nhân chuyên môn nào và theo trình tự nào. Nó cũng cung cấp lý do cho các quyết định định tuyến, giúp gỡ lỗi sau này.

*   Dữ liệu Agent xử lý việc điều tra dữ liệu thực tế. Nó làm phong phú thêm các lời nhắc bằng siêu dữ liệu bảng và cột, thực thi các truy vấn bằng các rào cản tích hợp, xác thực các lược đồ để tránh các lần quét không cần thiết và truy xuất dữ liệu mẫu.

*   Tìm kiếm Mã Agent theo dõi các chuyển đổi cột thông qua cơ sở mã, theo dõi dòng bảng qua nhiều bước chuyển đổi và tạo ra các giải thích bằng ngôn ngữ đơn giản về những gì mã đang thực hiện.

*   Agent theo yêu cầu theo dõi tình trạng sản xuất bằng cách tìm kiếm các thông báo ngừng hoạt động trên các kênh Slack, kiểm tra các nền tảng có thể quan sát để biết trạng thái quy trình và xác thực các số liệu chất lượng dữ liệu như số lượng rỗng và tỷ lệ trùng lặp.

*   Sau khi các chuyên gia hoàn thành công việc của họ, Công cụ tóm tắt Agent sẽ kết hợp những phát hiện của họ thành một câu trả lời mạch lạc. Điều này còn hơn cả sự ghép nối. Nó xử lý thông tin xung đột giữa các tác nhân, đảm bảo tính nhất quán và tạo ra phản hồi có cấu trúc sẵn sàng để con người xem xét.

Lộ trình nâng cao xử lý các yêu cầu thay đổi mọi thứ, chẳng hạn như thêm cột mới hoặc sửa đổi logic tổng hợp. Đây là các hoạt động ghi tiếp xúc với quy trình sản xuất, do đó về cơ bản kiến ​​trúc thận trọng hơn.

Một cải tiến duy nhất Agent xử lý các yêu cầu này. Nó đọc phiếu JIRA, phát hiện mã có liên quan trong kho lưu trữ, chạy kiểm tra xác thực, tạo các thay đổi lược đồ và sửa đổi mã, đồng thời tạo yêu cầu hợp nhất với tài liệu đầy đủ. Sau đó, người dùng có thể kích hoạt các đường dẫn thử nghiệm chạy qua bot. Nhưng ở mọi giai đoạn, kỹ sư con người đều xem xét và phê duyệt. Quy trình này được thiết kế bán tự động vì việc thay đổi mã đối với quy trình sản xuất đòi hỏi sự đánh giá của con người và hệ thống được xây dựng để tôn trọng ranh giới đó.

Để biết cách thức hoạt động của lộ trình điều tra trong thực tế, hãy xem xét một tình huống thực tế từ blog:

*   Ai đó nhắn tin cho nhóm trên Slack và hỏi tại sao không thể đọc được ID trong bảng phương tiện.

*   Ở thế giới cũ, một kỹ sư sẽ dành vài giờ tiếp theo để tìm kiếm danh mục, truy tìm dòng dõi, chạy SQL và kiểm tra nhật ký.

*   Với hệ thống đa tác nhân, Trình phân loại định tuyến câu hỏi đến cả ba tác nhân điều tra.

*   Dữ liệu Agent truy vấn dữ liệu thực tế và phát hiện ra rằng ID là UUID hợp lệ ở định dạng thập lục phân tiêu chuẩn. Nó cũng tìm kiếm danh mục dữ liệu của Grab và tìm thấy bảng thứ nguyên ánh xạ các UUID này thành tên xe mà con người có thể đọc được.

*   Tìm kiếm mã Agent theo dõi dòng dõi thông qua cơ sở mã và xác nhận rằng định dạng UUID đến trực tiếp từ hệ thống nguồn mà không áp dụng chuyển đổi Spark trong suốt quá trình.

*   Agent khi gọi sẽ kiểm tra trạng thái đường ống Luồng khí, các kênh Slack để tìm sự cố cũng như số liệu chất lượng dữ liệu và nhận thấy mọi thứ đều ổn.

*   Trình tóm tắt tập hợp tất cả lại thành một câu trả lời rõ ràng. Lỗi được cho là thực sự đã hoạt động như thiết kế.

Xem sơ đồ dưới đây:

[![Image 9](https://substackcdn.com/image/fetch/$s_!y-i5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bc2d863-e593-422b-a450-a6825d7cdfa7_2086x2226.png)](https://substackcdn.com/image/fetch/$s_!y-i5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bc2d863-e593-422b-a450-a6825d7cdfa7_2086x2226.png)

Mỗi đại lý hỏi một loại câu hỏi khác nhau. Dữ liệu trông như thế nào? Nó được biến đổi như thế nào? Hệ thống có khỏe mạnh không? Bức tranh đầy đủ chỉ xuất hiện khi những phát hiện của họ được kết hợp.

Kiến trúc này hoạt động tốt trong các bản demo được kiểm soát. Sau đó, người dùng thực sự bắt đầu sử dụng nó và nhóm phát hiện ra rằng tác nhân xây dựng chỉ là một phần của thử thách.

## Những thách thức trong sản xuất

Nguyên mẫu ban đầu của Grab hoạt động tốt trong các cài đặt được kiểm soát, nhưng việc sử dụng trong thế giới thực đã bộc lộ những lỗ hổng nghiêm trọng. Những câu hỏi phức tạp, những cuộc trò chuyện dài và những trường hợp khó khăn đã thúc đẩy hệ thống theo những cách mà bản demo chưa bao giờ làm được.

Dưới đây là bốn trong số những thách thức mang tính hướng dẫn nhất mà họ phải đối mặt, cùng với các giải pháp mà họ đã thiết kế.

[![Image 10](https://substackcdn.com/image/fetch/$s_!ittf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31beb73a-3d93-40dc-81fe-e9fda6ab5bce_2608x3102.png)](https://substackcdn.com/image/fetch/$s_!ittf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31beb73a-3d93-40dc-81fe-e9fda6ab5bce_2608x3102.png)

Chúng ta hãy xem xét từng chi tiết hơn:

### Bối cảnh tràn qua Agent Chuyển giao

Trong hệ thống đa tác nhân, ngữ cảnh được tích lũy nhanh chóng. Mỗi phần thông tin được truyền từ tác nhân này sang tác nhân tiếp theo sẽ thêm mã thông báo và hiệu suất LLM sẽ giảm khi cửa sổ ngữ cảnh bị quá tải.

Grab đã xây dựng một giải pháp đa lớp.

Họ theo dõi số lượng mã thông báo của mọi tin nhắn trong thời gian thực bằng cách sử dụng tiktoken, thư viện mã thông báo nguồn mở. Khi đạt đến giới hạn mã thông báo, các tin nhắn trước đó sẽ tự động được tóm tắt trong khi các tin nhắn gần đây và ngữ cảnh quan trọng vẫn được giữ nguyên để duy trì độ chính xác.

Họ cũng cắt bớt đầu ra của công cụ trước khi chuyển giao. Thay vì chuyển các tệp mã đầy đủ tới Tìm kiếm mã Agent, các mô hình LLM nhỏ hơn chỉ trích xuất các đoạn mã có liên quan và một mô tả ngắn. Người điều phối ngồi giữa các tác nhân, dọn dẹp và nén bối cảnh ở mỗi lần chuyển giao.

### Công cụ phình to

Thiết kế ban đầu cung cấp cho các tác nhân quyền truy cập vào hơn 30 công cụ, mỗi công cụ có mô tả chi tiết có cấu trúc giống như tài liệu API chung.

Vì các định nghĩa công cụ là một phần trong lời nhắc của tác nhân nên mọi lệnh gọi suy luận đều phải xử lý tất cả văn bản đó. Điều này làm suy giảm cả tốc độ và chất lượng.

Cách khắc phục là đơn giản hóa mạnh mẽ. Chỉ bao gồm các phần mô tả công cụ cần thiết cho việc ra quyết định, cắt bớt các đầu ra dài dòng và hợp lý hóa mọi thứ để ngắn gọn và có thể thực hiện được. Điều này nghe có vẻ đơn giản nhưng nó tạo ra sự cải thiện đáng kể về khả năng đáp ứng của hệ thống. Bài học là thiết kế công cụ là một mối quan tâm kỹ thuật quan trọng và ít công cụ được thiết kế tốt sẽ hoạt động tốt hơn một bộ sưu tập lớn các công cụ chung.

### Thực thi mã rủi ro

Các tác nhân AI có khả năng truy cập cơ sở dữ liệu và tạo mã gây ra rủi ro thực sự. Nếu không có biện pháp bảo vệ, họ có thể truy cập dữ liệu PII nhạy cảm, thực thi các hoạt động SQL nguy hiểm, chạy các truy vấn tốn kém để quét toàn bộ bảng hoặc tạo ra các thay đổi mã vi phạm.

Grab đã xây dựng bốn lớp phòng thủ phối hợp với nhau để các điểm mù của bất kỳ lớp nào cũng được che phủ bởi các lớp khác.

*   Lớp đầu tiên là phân loại đầu vào. Trình phân loại phát hiện các yêu cầu PII và các truy vấn ngoài phạm vi trước khi bất kỳ tác nhân nào thực thi.

*   Lớp thứ hai là xác thực SQL. Mọi truy vấn đều được kiểm tra để truy cập cột PII, các hoạt động nguy hiểm như DELETE hoặc DROP, bộ lọc phân vùng bị thiếu và tính hợp lệ của lược đồ. Nếu không có các bộ lọc phân vùng này, một truy vấn có thể quét toàn bộ một bảng lớn thay vì chỉ phần có liên quan, điều này vừa tốn kém, chậm và vừa tốn kém tính hợp lệ của lược đồ.

*   Lớp thứ ba là bảo vệ thời gian chờ, trong đó các giới hạn thực thi nghiêm ngặt đối với tất cả các truy vấn cơ sở dữ liệu sẽ ngăn chặn các hoạt động chạy trốn.

*   Lớp thứ tư là kiểm soát nâng cao. Tính năng nâng cao Agent không thể cam kết trực tiếp với các nhánh chính. Tất cả các thay đổi đều cần có sự xem xét của con người và mọi thứ đều diễn ra theo giai đoạn trước khi sản xuất.

### Kiếm được sự tin tưởng của người dùng

Ngay cả với các lớp an toàn, tác nhân AI vẫn có thể tạo ảo giác, hiểu sai câu hỏi hoặc vấp phải các trường hợp nguy hiểm. Nếu người dùng mất niềm tin vào câu trả lời, hệ thống sẽ thất bại bất kể khả năng kỹ thuật của nó như thế nào.

Grab đã xây dựng một hệ thống đánh giá con người, trong đó các kỹ sư có thể thực hiện năm hành động đối với bất kỳ phản hồi nào do AI tạo ra. Họ có thể phê duyệt nguyên trạng với chú thích cuối trang đã được xác minh, từ chối và ghi nhật ký để cải thiện, tinh chỉnh bằng cách thêm lời nhắc để tạo lại câu trả lời, định tuyến lại câu trả lời đến một tổng đài viên cụ thể với ngữ cảnh bổ sung hoặc chú thích bằng phản hồi có cấu trúc để liên tục cải tiến.

Họ cũng đã thực hiện một bước tiến hóa thiết kế quan trọng ở đây.

Ban đầu, hệ thống giữ lại tất cả các phản hồi do AI tạo ra cho đến khi được kỹ sư phê duyệt. Điều này an toàn nhưng chậm và tạo ra một nút thắt cổ chai mới khiến các câu hỏi không được giải đáp trong thời gian khối lượng công việc cao điểm.

Họ đã thiết kế lại quy trình để đăng phản hồi ngay lập tức với nhãn rõ ràng, chưa được xem xét, cho phép các kỹ sư xem xét và sửa đổi nếu cần. Người dùng nhận được câu trả lời nhanh chóng, tính minh bạch của nhãn đặt ra những kỳ vọng phù hợp và quá trình xem xét vẫn phát hiện ra lỗi.

Việc giải quyết những thách thức này đã làm cho hệ thống trở nên đáng tin cậy. Nhưng nhóm còn muốn thứ gì đó hơn thế nữa, một hệ thống ngày càng thông minh hơn theo thời gian

## Đóng vòng lặp

Các chú thích từ sự đánh giá của con người ban đầu là những bản ghi thụ động. Nhóm có rất nhiều thông tin về điều gì hiệu quả và điều gì thất bại, nhưng họ thiếu một phương pháp có hệ thống để học hỏi từ đó.

Họ đã chuyển đổi các chú thích thành một công cụ cải tiến tích cực thông qua nhiều cơ chế như sau:

*   Các chú thích ngẫu nhiên được lấy ra để tạo các trường hợp thử nghiệm nhằm đánh giá ngoại tuyến, đảm bảo hệ thống được kiểm tra dựa trên các lỗi trong thế giới thực thay vì các lỗi tổng hợp.

*   Phân tích mẫu xác định các vấn đề mang tính hệ thống bằng cách đặt các câu hỏi như:

    *   Trình phân loại có liên tục định tuyến tới các tác nhân sai không?

    *   Một tác nhân cụ thể có gặp khó khăn với các loại truy vấn nhất định không?

    *   Các lược đồ bảng cụ thể có gây nhầm lẫn không?

*   Số liệu chất lượng được theo dõi theo thời gian phát hiện sự hồi quy. Nếu tỷ lệ từ chối đột ngột tăng đột biến thì có điều gì đó đã thay đổi cần được điều tra.

*   Các cải tiến có mục tiêu sử dụng những thông tin chi tiết này để tinh chỉnh lời nhắc của tổng đài viên, nâng cao các biện pháp bảo vệ và thêm ví dụ cho các loại truy vấn mà hệ thống gặp khó khăn.

Tác động rất đáng kể. Các bot hiện tự động xử lý phần lớn các yêu cầu của người dùng thông thường và một phần đáng kể các yêu cầu nâng cao. Thời gian phân giải giảm theo một mức độ lớn. Nhóm đã lấy lại được một số băng thông kỹ thuật có giá trị tương đương toàn thời gian, chuyển hàng trăm giờ từ hỗ trợ phản ứng sang cung cấp lộ trình chủ động.

## Phần kết luận

Hành trình của Grab từ một kỹ sư dữ liệu đầy rẫy đến một nhóm được tăng cường AI đã chắt lọc thành một số nguyên tắc chính:

*   Nếu các vấn đề khác nhau nhưng quá trình giải quyết chúng vẫn nhất quán thì đó là cơ hội tốt để áp dụng tự động hóa.

*   Khi xây dựng quá trình tự động hóa đó, phần lớn nỗ lực sẽ dồn vào việc tăng cường sản xuất hơn là bản thân các tác nhân.

*   Áp dụng các mức độ tự chủ khác nhau dựa trên hồ sơ rủi ro của hoạt động.

*   Các cuộc điều tra chỉ đọc có thể được thực hiện với sự giám sát nhẹ nhàng, nhưng bất cứ điều gì thay đổi dữ liệu sản xuất đều phải có sự giám sát của con người.

*   Thiết kế vòng phản hồi một cách có chủ ý, vì nếu không có nó, hệ thống sẽ bị đóng băng ở mức chất lượng của lần triển khai đầu tiên. Mọi phản hồi bị từ chối, mọi chú thích, mọi mẫu trong dữ liệu lỗi đều là cơ hội để làm cho hệ thống thông minh hơn.

Những nguyên tắc riêng của Grab đã nắm bắt được điều này rất tốt. Mục tiêu không bao giờ là thay thế các kỹ sư. Đó là để trả lại thời gian cho họ.

**Tài liệu tham khảo:**

*   [Từ chữa cháy đến xây dựng: AI Agents khôi phục năng suất cốt lõi của nhóm chúng tôi như thế nào](https://engineering.grab.com/from-firefighting-to-building)

*   [AI Agent là gì](https://en.wikipedia.org/wiki/AI_agent)
