---
title: "Workflow lab: Code to canvas – Figma Learn - Help Center"
category: "Art of Programming Computer"
categoryOrder: 2
order: 4
source: "https://help.figma.com/hc/en-us/articles/40219873508247-Workflow-lab-Code-to-canvas?utm_campaign=051826+-+Activation+-+Wor&utm_content=051826+-+Activation+-+Wor&utm_medium=email&utm_source=figma"
sourceLabel: "Figma Help"
---

Lưu ý: Khi nào nên sử dụng điều này: Sử dụng quy trình công việc này khi bạn muốn các công cụ tổng đài của mình tạo mã tham chiếu các thành phần thực và mã thông báo từ hệ thống thiết kế của bạn.

Hệ thống thiết kế cho phép các nhóm tạo ra những trải nghiệm nhất quán, gắn kết trên quy mô lớn. Nhưng khi công việc thiết kế diễn ra trong mã, chẳng hạn như trong tuần hack, thử nghiệm nhanh hoặc chạy nước rút được AI hỗ trợ, những thay đổi đó có thể trở thành công việc thực sự chỉ tồn tại trong cơ sở mã của bạn, bị ngắt kết nối với hệ thống thiết kế trong Figma.

Quy trình công việc này cho thấy cách đưa một thiết kế dựa trên mã (cùng với các biến của nó) lên khung vẽ Figma, đánh giá và tinh chỉnh nó cũng như đẩy các mã thông báo đã cập nhật trở lại mã. giữ cho thiết kế và phát triển được đồng bộ.

#### Kỹ năng nền tảng

Các kỹ năng `/figma-generate-design` và `/figma-generate-library` được sử dụng trong quy trình làm việc này được cài đặt sẵn với máy chủ MCP của Figma. Không cần cài đặt thủ công.

#### Bước 1: Đưa thiết kế và các biến của bạn vào Figma

Nếu bạn đã xây dựng hướng thiết kế mới trong mã, chẳng hạn như chế độ tối sử dụng các biến màu từ hệ thống thiết kế hiện tại của mình, bạn có thể sử dụng các kỹ năng được cài đặt sẵn để nắm bắt hướng đó trong Figma.

Chạy lời nhắc trong nhân viên hỗ trợ của bạn để gọi các kỹ năng `/figma-generate-design` và `/figma-generate-library`.

Điều này sẽ:

*   Đặt màn hình của bạn trên canvas Figma (ví dụ: chế độ sáng và tối cạnh nhau)
*   Tạo bộ sưu tập biến mới trong bảng biến phản ánh mã thông báo được sử dụng trong mã của bạn

Từ đây, bạn có thể đánh giá nhanh thiết kế và xem nó hoạt động như thế nào trên các màn hình, một điều rất khó đánh giá khi thiết kế chỉ tồn tại trong môi trường cục bộ đang chạy.

#### Bước 2: Đánh giá và tinh chỉnh các biến của bạn

Với màn hình và các biến của bạn trên khung vẽ, hãy xem lại thiết kế để tìm các vấn đề khó nắm bắt chỉ bằng mã. Những điều phổ biến cần tìm:

*   **Cường độ màu:** Màu nhấn thương hiệu hoạt động tốt ở chế độ sáng có thể trông quá bão hòa hoặc màu neon ở chế độ tối. Hãy cân nhắc việc đổi sang màu sắc hoặc tông màu khác trong bảng màu của bạn để tạo cảm giác cân bằng hơn.
*   **Độ tương phản của văn bản:** Văn bản có độ tương phản thấp, đặc biệt là các nhãn phụ như ngày tháng hoặc chú thích, có thể không đáp ứng các tiêu chuẩn về khả năng truy cập. Nếu đội của bạn nhắm mục tiêu WCAG AAA, hãy kiểm tra cẩn thận các giá trị này.

Để thực hiện điều chỉnh, hãy mở bảng biến và cập nhật trực tiếp các mã thông báo có liên quan. Các thay đổi được phản ánh theo thời gian thực trên tất cả các thành phần và tham chiếu kiểu trên canvas, mang lại cho bạn cái nhìn toàn cảnh rõ ràng về cách các quyết định về mã thông báo ảnh hưởng đến thiết kế đầy đủ.

Mẹo: Xem các biến và hiệu ứng của chúng cùng một lúc, thay vì cập nhật giá trị trong mã và làm mới trình duyệt, giúp việc lặp lại nhanh hơn đáng kể.

#### Bước 3: Đẩy mã thông báo đã tinh chỉnh trở lại mã

Khi các biến của bạn đã ở vị trí phù hợp, hãy nhắc đại lý của bạn cập nhật hệ thống thiết kế trong cơ sở mã của bạn bằng các mã thông báo đã được tinh chỉnh. Điều này giúp mã của bạn và các tệp Figma được đồng bộ hóa, trong đó Figma là nguồn thông tin chính xác cho các quyết định thiết kế.

#### Tóm tắt lại

Trong quy trình làm việc này, bạn:

1.   Đã sử dụng các kỹ năng `/figma-generate-design` và `/figma-generate-library` để đưa thiết kế dựa trên mã và các biến của nó lên canvas Figma.
2.   Đánh giá thiết kế trên nhiều màn hình và xác định các vấn đề về màu sắc và khả năng truy cập.
3.   Các giá trị biến được tinh chỉnh trực tiếp trong Figma, với những thay đổi được phản ánh theo thời gian thực.
4.   Đã đẩy các mã thông báo đã cập nhật trở lại mã để giữ cho thiết kế và quá trình phát triển được đồng bộ hóa.

Người đại diện xử lý công việc lập bản đồ tẻ nhạt. Canvas đưa ra các quyết định thiết kế nhanh hơn và dễ dàng hơn để thực hiện đúng.

### Đi sâu và rộng với AI, ngay từ Figma

[Video 9](https://www.youtube.com/watch?v=11mdb7lLclM)
Đã có thiết kế trên Figma và muốn khám phá những ý tưởng mới? Bạn có thể sử dụng tác nhân để tạo hướng dẫn thay thế trực tiếp trên canvas bằng cách sử dụng các thành phần, biến và kiểu hiện có của mình. Thay vì bắt đầu từ đầu, tác nhân xây dựng bằng nội dung hệ thống thiết kế thực của bạn để tạo ra các màn hình và biến thể mới.

Lưu ý: Khi nào nên sử dụng quy trình này: Sử dụng quy trình công việc này khi bạn muốn nhanh chóng khám phá hoặc lặp lại các thiết kế hiện có mà không cần rời khỏi Figma.

Đối với nhiều đội, Figma là nguồn gốc của sự thật. Các thiết kế đã tồn tại trên canvas và thử thách không phải bắt đầu từ đầu mà là biết cách tiến về phía trước. Khi nghiên cứu của người dùng phát hiện ra một vấn đề với màn hình hiện có, phần khó nhất của quá trình lặp lại thường là thực hiện bước đầu tiên đó.

Quy trình công việc này cho thấy cách sử dụng tác nhân để tạo hướng bắt đầu thô bằng cách sử dụng các thành phần thực của bạn, để bạn có thể phản ứng với điều gì đó cụ thể và tinh chỉnh nó trên canvas.

#### Bước 1: Xác định vấn đề

Bắt đầu bằng một tuyên bố vấn đề rõ ràng, dựa trên nghiên cứu hoặc phản hồi của người dùng. Lời nhắc của bạn càng cụ thể thì kết quả đầu ra của nhân viên sẽ càng hữu ích.

Ví dụ: bảng thông tin doanh thu của khách hàng trong đó trạng thái gia hạn được hiển thị dưới dạng nhãn văn bản thuần túy ở cuối mỗi hàng. Nghiên cứu cho thấy người dùng bỏ lỡ nó. Vấn đề cần giải quyết là làm cho sức khỏe đổi mới trở nên nổi bật hơn và dễ dàng hành động hơn.

Thường có nhiều cách tiếp cận hợp lệ cho một vấn đề như thế này, như mã hóa màu sắc, nhóm các hàng theo trạng thái hoặc giới thiệu một hệ thống phân cấp trực quan mới. Xem chỉ đường trên khung vẽ là điều giúp cuộc trò chuyện tiến về phía trước.

#### Bước 2: Tạo hướng xuất phát với tác nhân

Trong đại lý của bạn, hãy chạy kỹ năng `/figma-use`. Đưa bối cảnh có liên quan vào lời nhắc của bạn, chẳng hạn như thông tin chi tiết về nghiên cứu người dùng, vấn đề cụ thể và bất kỳ hạn chế nào, sau đó yêu cầu nhân viên hỗ trợ khám phá cách tiếp cận bằng cách sử dụng các thành phần hiện có của bạn.

Tác nhân sẽ tạo ra một bản lặp thô trực tiếp trên canvas, được xây dựng bằng các thành phần sản xuất của bạn.

Lưu ý: Mục tiêu ở giai đoạn này không phải là một thiết kế đã hoàn thiện. Đó là điểm khởi đầu cụ thể mà bạn có thể phản ứng và tinh chỉnh.

#### Bước 3: Tinh chỉnh trên canvas

Xem lại những gì tác nhân đã tạo ra và sử dụng nó làm điểm khởi đầu. Một số điều cần đánh giá:

*   **Giải pháp này có làm thay đổi nguyên tắc tổ chức của bố cục không?** Việc nhóm hoặc ưu tiên thông tin theo cách khác nhau có thể khiến dữ liệu quan trọng trở thành thứ đầu tiên người dùng nhìn thấy, thay vì thứ họ phải quét tìm.
*   **Có sử dụng đúng thành phần không?** Tác nhân phải được lấy từ hệ thống thiết kế của bạn. Nếu không, hãy điều chỉnh lời nhắc của bạn hoặc hoán đổi các thành phần theo cách thủ công.
*   **Điều gì hiệu quả và điều gì không?** Phản ứng với những gì trước mắt bạn. Người đại diện giúp bạn vượt qua trang trống; bạn và nhóm của bạn đưa ra đánh giá về thiết kế.

Việc lặp lại trực tiếp trên khung vẽ thay vì nhắc lại nhiều lần cho phép bạn chuyển từ cuộc thảo luận trừu tượng sang các quyết định cụ thể, rõ ràng một cách nhanh chóng.

#### Tóm tắt lại

Trong quy trình làm việc này, bạn:

1.   Xác định một vấn đề thiết kế dựa trên nghiên cứu người dùng.
2.   Đã sử dụng kỹ năng `/figma-use` để tạo hướng thô trên khung vẽ bằng cách sử dụng các thành phần sản xuất thực.
3.   Phản ứng với kết quả đầu ra và cộng tác cải tiến nó, đưa ra giải pháp mạnh mẽ hơn nhanh hơn so với việc bắt đầu lại từ đầu.

### Đặt tất cả lại với nhau

Trên cả ba quy trình công việc, đều có một mẫu giống nhau: cho dù bạn bắt đầu bằng mã hay bắt đầu trên canvas, thì tác nhân sẽ xử lý giàn giáo. Bạn dành thời gian cho công việc đòi hỏi con mắt của một nhà thiết kế.

| Quy trình làm việc | Điểm xuất phát | Kỹ năng then chốt | Kết quả |
| --- | --- | --- | --- |
| 1. Mã vào canvas | Nguyên mẫu trong mã | `/prototype-to-figma` | Màn hình được nhập dưới dạng khung thiết kế, sẵn sàng tinh chỉnh |
| 2. Thiết kế đồng bộ hệ thống | Chế độ tối được tích hợp sẵn trong mã | `/figma-generate-design`, `/figma-generate-library` | Các biến và màn hình trong Figma, mã thông báo được đẩy trở lại mã |
| 3. Khám phá canvas | Thiết kế Figma hiện có | `/figma-use` | Agent hướng được tạo bằng cách sử dụng các thành phần thực, được tinh chỉnh trên canvas |

## Tiếp tục học hỏi

*   [Bắt đầu với máy chủ Figma MCP](https://help.figma.com/hc/en-us/articles/39216419318551)
*   [Hướng dẫn về máy chủ Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559)
*   [Kỹ năng Figma cho MCP](https://help.figma.com/hc/en-us/articles/39166810751895)
*   [Thiết lập kết nối mã](https://help.figma.com/hc/en-us/articles/14606897474647)
