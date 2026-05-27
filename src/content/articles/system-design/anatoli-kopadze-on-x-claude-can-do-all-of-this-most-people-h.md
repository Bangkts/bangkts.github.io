---
title: "Anatoli Kopadze on X: 'Claude Can Do All of This. Most People Have No Idea.' / X"
category: "System Design"
categoryOrder: 1
order: 8
source: "https://x.com/AnatoliKopadze/status/2057813254617858078"
sourceLabel: "ByteByteGo"
---

Luôn cho rằng độc giả của tôi biết những điều cơ bản. Đừng giải thích LLM là gì hoặc blockchain là gì.

Khi tôi chia sẻ một chủ đề hoặc bài viết, công việc của bạn là:
1. Xác định 3 góc độ phản trực giác hoặc đáng ngạc nhiên nhất
2. Tìm kết nối tới các sự kiện gần đây mà tôi có thể đã bỏ lỡ
3. Đề xuất cách tôi có thể coi đây là một câu chuyện chứ không phải một bản tóm tắt

Giọng điệu: trực tiếp, không ngôn ngữ doanh nghiệp, không cụm từ lấp chỗ trống.
Định dạng: đoạn văn ngắn, không có dấu đầu dòng trừ khi tôi yêu cầu.
Đừng bao giờ bắt đầu câu trả lời bằng "Câu hỏi hay" hoặc "Chắc chắn".
```

2. Artifacts - working apps inside your chat

Many people think Claude can only produce text. It can't build anything real. That's wrong. Artifacts are when Claude builds something that actually works inside the chat. Not a block of code you have to copy somewhere - a live product in a side panel. A calculator, a habit tracker, a game, a dashboard with charts. You open it, click it, use it. Without leaving the conversation.

SVG graphics, interactive charts, Mermaid diagrams - all supported. Available on the free plan. Most people have never tried it.

Try this 

```văn bản
Xây dựng cho tôi một công cụ theo dõi thói quen dưới dạng một ứng dụng web đang hoạt động.

Tôi muốn theo dõi 5 thói quen hàng ngày.

Mỗi ngày tôi có thể kiểm tra chúng.

Hiển thị bộ đếm chuỗi 7 ngày cho mỗi thói quen.

Nếu tôi bỏ lỡ một ngày, chuỗi sẽ được đặt lại.

Thiết kế: nền tối, giao diện tối giản gọn gàng.

Tạo các hộp kiểm thỏa mãn khi nhấp chuột - thêm một hình ảnh động nhỏ khi tôi hoàn thành một hộp kiểm.

Dữ liệu sẽ vẫn tồn tại nếu tôi làm mới trang.
```

3. Adaptive Thinking - a different level of reasoning

Most Claude users have never turned this on. Extended Thinking is a mode where Claude reasons through a problem step by step before giving you an answer - and you can watch the entire process.

For simple questions, you don't need it. For complex decisions, strategic analysis, or any situation where you want Claude to actually think rather than pattern-match - the difference in output is significant.

Turn it on. Ask the same question you've been asking. Compare the answers.

[![Image 4: Image](https://pbs.twimg.com/media/HI3wWvAXMAAGiY5?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057564878143959040)

Use this when facing a real decision

```văn bản
Tôi đang quyết định giữa hai lựa chọn và tôi muốn bạn suy nghĩ kỹ điều này trước khi trả lời.

Phương án A: [mô tả phương án A]
Phương án B: [mô tả phương án B]

Tình huống của tôi: [bối cảnh của bạn, những hạn chế, điều quan trọng nhất]

Hãy giải quyết vấn đề này trước khi trả lời. Hãy suy nghĩ về:
- Hậu quả thứ hai và thứ ba của mỗi lựa chọn
- Những gì tôi có thể đang thừa cân hoặc thiếu cân về mặt cảm xúc
- Thông tin nào tôi có thể thiếu sẽ làm thay đổi quyết định
- Tùy chọn nào có khả năng bảo vệ nhược điểm tốt hơn nếu có sự cố xảy ra

Sau đó cho tôi lời khuyên thực tế của bạn với lý do của bạn.
```

4. Memory - Claude that knows who you are

With Memory on, Claude builds a profile of you over time. Your job, your projects, how you like to communicate, what you're currently working on.

Start a completely new chat and it already knows the context. You never introduce yourself again.

It's off by default. Most people don't know it exists

[![Image 5: Image](https://pbs.twimg.com/media/HI3yGMwXcAQ_J9H?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057566793095409668)

```văn bản
Tôi muốn bạn nhớ những điều sau đây về tôi để bạn không cần phải hỏi lại:

Tên tôi là [tên]. Tôi làm việc với [vai trò] tại [công ty hoặc dự án].
Trọng tâm chính của tôi lúc này là [những gì bạn đang làm].
Khán giả hoặc khách hàng của tôi là [họ là ai].

Khi tôi yêu cầu giúp đỡ, hãy luôn giả định bối cảnh này trừ khi tôi nói khác.
Phong cách giao tiếp ưa thích của tôi: [trực tiếp/chi tiết/thông thường/trang trọng].
Những điều tôi thấy khó chịu khi trả lời: [ví dụ: dấu đầu dòng, phần giới thiệu dài, cảnh báo quá mức].

Lưu tất cả điều này vào bộ nhớ bây giờ.
```

## Give Claude a role - one prompt changes everything

Claude doesn't have to be "an AI assistant." Give it a specific role and it commits fully - changing how it questions you, what it pushes back on, and what it refuses to let slide. Copy any prompt below and paste it at the start of a new chat.

5. Personal psychologist

Most people use Claude as a validation machine. They describe a problem. Claude says that sounds hard and offers five bullet points of advice.

That's not how good therapy works. This prompt turns Claude into something closer to a CBT therapist - one that asks questions instead of giving answers, and challenges your thinking instead of validating it.

Useful for decisions you keep going back and forth on, anxiety you can't pin down, or any situation where you need a clear outside perspective.

```văn bản
Bạn là một nhà trị liệu hành vi nhận thức với 20 năm kinh nghiệm. Tôi sẽ chia sẻ điều gì đó mà tôi đang gặp khó khăn.

Cách tiếp cận của bạn:
- Đừng đưa ra lời khuyên ngay lập tức. Bắt đầu bằng cách đặt câu hỏi để giúp tôi hiểu cách suy nghĩ của chính mình.
- Hãy lắng nghe những biến dạng về nhận thức - thảm họa, suy nghĩ đen trắng, đọc suy nghĩ, bói toán - và chỉ ra chúng khi bạn nhận thấy chúng.
- Hỏi một câu hỏi tại một thời điểm. Đừng áp đảo tôi.
- Khi tôi tự mình đi đến kết luận thông qua câu hỏi của bạn, đó chính là mục tiêu. Đừng đưa cho tôi câu trả lời.
- Hãy ấm áp nhưng trung thực. Đừng xác nhận tôi nếu suy nghĩ của tôi rõ ràng bị bóp méo.
- Nếu tôi dường như đang tránh điều gì đó quan trọng, hãy trực tiếp nêu tên nó.

Đừng bắt đầu bằng phần giới thiệu lâm sàng. Chỉ cần hỏi tôi chuyện gì đang xảy ra.
```

6. The hard mentor

By default Claude agrees with you. It adds to your ideas, supports your reasoning, finds the positives. This is almost always the wrong thing.

This prompt disables that. Claude stops validating and starts stress-testing. It finds the weak assumptions, the missing considerations, the exact places your plan breaks.

It's uncomfortable. That's why it works.

```văn bản
Bạn là một người cố vấn trung thực đến mức tàn nhẫn. Bạn đã xây dựng và thất bại ở nhiều công ty. Bạn đã chứng kiến ​​hàng trăm người mắc lỗi tương tự với sự tự tin hoàn toàn.

Công việc của bạn không phải là khuyến khích tôi - mà là bảo vệ tôi khỏi những điểm mù của chính mình trước khi tôi phạm phải sai lầm đắt giá.

Quy tắc:
- Không đồng ý với tôi khi bạn cho rằng tôi sai. Hãy cụ thể về lý do tại sao.
- Chỉ ra những điều tôi không thấy, đặc biệt là những điều tôi có thể tránh né vì tôi muốn kế hoạch của mình thành công.
- Hãy hỏi những câu hỏi khó mà tôi chưa từng nghĩ tới.
- Nếu điều gì đó là một ý tưởng tồi, hãy nói đó là một ý tưởng tồi. Đừng cân bằng nó với "mặt khác..."
- Kết thúc câu trả lời của bạn bằng điều quan trọng nhất mà tôi nên suy nghĩ trước khi tiếp tục.

Tôi sắp chia sẻ một ý tưởng. Đừng tử tế với nó.
```

7. Personal trainer

Generic fitness advice is everywhere. It doesn't account for your schedule, your injuries, your equipment, your actual goals.

Give Claude your real numbers and it builds a real plan. Not a template. Not something you could find on any fitness website. A program built around your situation, that adjusts when you report back what's working.

```văn bản
Bạn là một huấn luyện viên cá nhân chuyên nghiệp và chuyên gia dinh dưỡng thể thao. Tôi muốn bạn xây dựng cho tôi một chương trình đào tạo hoàn chỉnh.

Tình hình của tôi:
Tuổi: [tuổi]
Cân nặng/thành phần cơ thể hiện tại: [chi tiết]
Mục tiêu: [giảm mỡ / xây dựng cơ bắp / cải thiện sức bền / thể lực nói chung]
Thiết bị có sẵn: [phòng tập thể dục / tại nhà / chỉ có tạ / v.v.]
Số ngày mỗi tuần tôi có thể tập luyện: [number]
Thời gian mỗi phiên: [phút]
Bất kỳ thương tích hoặc hạn chế nào: [chi tiết hoặc "không có"]
Trình độ thể lực hiện tại: [sơ cấp/trung cấp/cao cấp]

Xây dựng cho tôi một chương trình 12 tuần. Cung cấp cho tôi kế hoạch đầy đủ cho mỗi tuần với các bài tập, hiệp, số lần lặp và thời gian nghỉ ngơi. Giải thích lý do tại sao bạn cấu trúc nó theo cách này - Tôi muốn hiểu logic chứ không chỉ làm theo hướng dẫn. Sau khi bắt đầu, tôi sẽ báo cáo lại hàng tuần và bạn sẽ điều chỉnh dựa trên diễn biến của nó.
```

8. Practice a difficult conversation

Most people walk into hard conversations unprepared. They know what they want to say but not what the other person will actually say back.

Claude plays the other person. Realistically. It responds the way they would respond, pushes back when your argument is weak, and makes you earn a good outcome. After you practice a few times, the real conversation is easier.

```văn bản
Tôi cần chuẩn bị cho một cuộc trò chuyện khó khăn. Tôi muốn bạn đóng vai người khác để tôi có thể luyện tập.

Người đó: [mô tả họ là ai - ông chủ, khách hàng, người đồng sáng lập, v.v.]
Điều tôi cần nói: [điều bạn cần hỏi hoặc nói với họ]
Tại sao nó khó: [điều bạn sợ/điều gì có thể xảy ra]
Người này là người như thế nào: [tính cách của họ, cách họ thường phản ứng, họ quan tâm đến điều gì]

Giữ nguyên tính cách trong suốt cuộc trò chuyện. Hãy trả lời theo cách mà người này thực sự sẽ phản hồi - không phải theo cách tôi muốn họ làm. Nếu tôi nói điều gì đó yếu đuối hoặc không thuyết phục, hãy phản bác lại điều đó.

Sau mỗi cuộc trao đổi, hãy thoát ra khỏi nhân vật một cách ngắn gọn để cho tôi biết điều gì hiệu quả và điều gì không - sau đó quay lại. Cuối cùng, hãy đưa ra bản tóm tắt đầy đủ cho tôi: điều tôi đã làm tốt, điều gì cần thay đổi và những điều quan trọng nhất cần ghi nhớ cho cuộc trò chuyện thực sự.

Bắt đầu trong nhân vật. Đợi tôi mở cửa.
```

9. Devil's advocate

You've made up your mind. You've already thought through the objections. You're convinced.

That's exactly the moment to have Claude attack the decision. Not polite concerns. The full case against it. The three most realistic ways it fails. The things you're not seeing because you want it to work.

Five minutes now. Before you commit. Not after.

```văn bản
Tôi đã đưa ra quyết định và tôi muốn bạn xây dựng cơ sở vững chắc nhất có thể để chống lại quyết định đó trước khi tôi cam kết.

Quyết định: [mô tả chính xác những gì bạn dự định làm]
Lý do của tôi: [tại sao bạn nghĩ đó là một ý tưởng hay]
Điều tôi đã cân nhắc: [những phản đối mà bạn đã nghĩ đến]

Công việc của bạn:
- Xây dựng trường hợp mạnh mẽ nhất có thể CHỐNG LẠI quyết định này.
- Đừng cân bằng nó với những mặt tích cực. Tôi đã tin vào điều đó rồi - tôi cần phản biện.
- Tìm những giả định mà tôi đang đưa ra có thể sai.
- Mô tả 3 cách thực tế nhất mà điều này không thành công hoặc phản tác dụng.
- Hãy cho tôi biết những gì tôi có thể đang đánh giá thấp.
- Hãy cho tôi biết tôi cần phải tin vào điều gì để đây thực sự là một ý tưởng tồi.

Hãy tàn nhẫn. Nếu đây là một sai lầm thì tôi cần phải biết ngay bây giờ.
```

## Product features most people don't know exist

10. Claude in Chrome - Claude that sees what you see

Most people use Claude in a separate tab and manually copy-paste what they need. That's the hard way.

Claude in Chrome is a browser extension that gives Claude full visibility into your active tab and the ability to act on it. It reads the page, clicks links, fills forms, navigates to new URLs. You describe the task in plain English and step away.

Search Claude for Chrome in the Chrome Web Store → install → sign in with your Claude account. Click the extension icon to open the sidebar. Claude can now see and interact with any page you have open.

Example task to give it

```văn bản
Tôi đang ở trang danh sách việc làm này.

Xem qua mọi danh sách hiển thị và trích xuất: chức danh công việc, tên công ty, mức lương nếu được hiển thị và 3 yêu cầu hàng đầu.

Xây dựng cho tôi bảng so sánh sắp xếp theo mức lương, cao nhất xếp trước.

Nếu có nhiều trang, hãy nhấp qua trang tiếp theo và tiếp tục cho đến khi bạn xem hết tất cả các kết quả.
```

11. Claude Cowork - Claude that lives on your desktop

Claude on the web has no access to your computer. It can't see your files. You have to paste everything manually.

Cowork is a desktop app that gives Claude direct access to your file system. It reads your actual files, edits documents, creates new ones, organizes folders - without you copying anything into a chat box.

[![Image 6: Image](https://pbs.twimg.com/media/HI3znU_W8AIR2MD?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057568461753085954)

12. Scheduled Tasks - Claude that works while you sleep

Most people treat Claude as something they have to activate. Open a chat, type a request, wait for output, close the tab.

Scheduled Tasks change that. You set a task once and Claude executes it automatically at the time and frequency you choose - no trigger from you required. Every morning. Every Monday. Every hour. Claude runs it and saves the output to your folder.

[![Image 7: Image](https://pbs.twimg.com/media/HI33KXwXUAEB-78?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057572362325807105)

Example scheduled task description

```văn bản
Mỗi buổi sáng trong tuần vào lúc 7h30 sáng, hãy thực hiện như sau:
1. Tìm kiếm tin tức hàng đầu về AI và tiền điện tử trong 24 giờ qua
2. Chọn 5 câu chuyện quan trọng nhất - tập trung vào những điều gây ngạc nhiên, phản trực giác hoặc có ý nghĩa thực sự đối với các nhà xây dựng và nhà đầu tư
3. Đối với mỗi câu chuyện, hãy viết: tiêu đề, tóm tắt 2 câu, tại sao nó quan trọng
4. Lưu kết quả dưới dạng "brief-[date].md" trong thư mục /briefs của tôi

Giữ giọng điệu trực tiếp và phân tích. Không có lông tơ. Có thể đọc được trong 3 phút.
```

13. Skills in Cowork - install new capabilities like plugins

Skills are pre-built instruction sets that give Claude specific capabilities inside Cowork. Instead of explaining what you need every time, you install a skill once and Claude already knows how to handle that type of task - whether it's building PowerPoint files, working with PDFs, or running a specific workflow.

Think of it like apps on a phone. The base phone works without them. But with the right apps installed, it does a lot more. How to find and install: Cowork → Customize → Skills to see what's installed. To add new ones, click Browse plugins in the left sidebar → find a plugin → install it. The skills from that plugin appear in your Skills tab automatically and Claude uses them when the task calls for it.

[![Image 8: Image](https://pbs.twimg.com/media/HI7A9bHW0AAOCKD?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057794241238061056)

14. CLAUDE.md - rules Claude reads automatically every session

In Cowork and Claude Code, you can create a CLAUDE.md file in your project folder. Claude reads it at the start of every single session without being asked.

Your coding conventions. Your writing style rules. Terminology that means something specific in your company. Brand voice guidelines. Write it once. Claude follows it across every session in that project forever.

```văn bản
# Dự án: Bản tin AI

## Về dự án này
Bản tin hàng tuần về AI và tiền điện tử dành cho các nhà xây dựng và nhà đầu tư. 35.000 người đăng ký. Giọng điệu trực tiếp, phân tích, đôi khi bất kính.

## Quy tắc viết
- Đoạn văn ngắn. Tối đa 3 câu.
- Không có dấu đầu dòng trong nội dung biên tập. Chỉ văn xuôi.
- Không có dấu gạch ngang. Sử dụng dấu gạch nối hoặc cơ cấu lại câu.
- Những con số đánh bại tính từ. Viết "tiết kiệm 3 giờ" chứ không phải "tiết kiệm thời gian đáng kể".
- Không bao giờ sử dụng: "delve", "đột phá", "thay đổi trò chơi", "đòn bẩy" (như một động từ), "tận dụng".
- Các cơn co thắt là tốt và được khuyến khích.

## Quy tắc nội dung
- Giả sử người đọc biết LLM là gì. Đừng giải thích những điều cơ bản.
- Dẫn đầu bằng điều đáng ngạc nhiên hoặc phản trực giác nhất.
- Mỗi bài viết đều cần một câu “vậy thì sao” cụ thể - người đọc nên làm gì hoặc nghĩ khác đi.

## Cấu trúc tập tin
- Bản nháp đi vào / bản nháp
- Các bài viết đã xuất bản được đưa vào /published với tiền tố ngày: YYYY-MM-DD-title.md
- Ghi chú nghiên cứu được đưa vào /research
```

15. Claude Code - AI that writes, tests, and fixes code in your terminal

Some people still don't know you can write code with Claude. Not just snippets - full production-level code, entire features, complex refactors. You describe what you need in plain English and Claude writes it.

Claude Code takes that one step further. It works directly inside your development environment - not in a chat window. It reads your actual codebase, writes new code, runs tests, reads the error messages, and fixes the bugs in a loop until the task is done.

It integrates with VS Code and JetBrains. You can drop it into GitHub Actions and it will automatically review or write pull requests without you touching anything.

[![Image 9: Image](https://pbs.twimg.com/media/HI69Ep8aMAAAzx2?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057789967431249920)

16. Claude Design - AI for visual work

Most people don't know this product exists. Claude Design is a separate Anthropic Labs tool for visual work - product one-pagers, pitch decks, prototypes, landing page layouts.

You describe what you need. Claude builds it. Exports to PPTX, Canva, PDF, or HTML. For people who aren't designers, it replaces a 3-hour Figma session with a 10-minute conversatio

To get access, just head to 

[claude.ai/design](https://claude.ai/design)

 - that's the direct link to Claude Design, no extra steps needed.

[![Image 10: Image](https://pbs.twimg.com/media/HI7BhJDWgAAP27X?format=jpg&name=small)](https://x.com/AnatoliKopadze/article/2057813254617858078/media/2057794854864715776)

17 Prompt Caching - 90% cost reduction on API calls (DEV)

For developers building on the Claude API. If your requests include a large repeated context block - a long system prompt, a reference document, a codebase - you're paying to re-process those same tokens on every single call.

Prompt Caching stores that content server-side. Subsequent calls reuse the cache instead of re-processing it. Up to 90% cost reduction on cached tokens. Noticeably faster responses. If you're building at scale and not using this, you're leaving a significant amount of money on the table.

Add "cache_control": {"type": "ephemeral"} to the content block you want cached. Cache persists for 5 minutes and resets the timer on each use. Works for system prompts, large documents, and tool definitions. 

```văn bản
{
"model": "claude-opus-4-6",
"hệ thống": [
    {
"loại": "văn bản",
"text": "[tài liệu tham khảo hoặc lời nhắc hệ thống lớn của bạn]",
"cache_control": {"type": "phù du"}
    }
  ],
"tin nhắn": [
    {
"vai trò": "người dùng",
"content": "[tin nhắn của người dùng - điều này sẽ thay đổi mỗi cuộc gọi]"
    }
  ]
}

// System prompt được lưu vào bộ đệm sau cuộc gọi đầu tiên.
// Mỗi cuộc gọi tiếp theo trong vòng 5 phút sẽ sử dụng lại bộ đệm.
// Cache trúng = rẻ hơn 90% + phản hồi nhanh hơn.
```

Bây giờ bạn biết nhiều về Claude hơn hầu hết những người sử dụng nó hàng ngày.

Chọn một tính năng từ danh sách này. Chỉ một thôi. Hãy thiết lập nó ngay hôm nay. Bạn không cần phải triển khai mọi thứ cùng một lúc - biết những gì tồn tại đã là một nửa trận chiến.

Hãy quay lại bài viết này khi bạn đã sẵn sàng cho bài viết tiếp theo.

Bạn muốn xuất bản bài viết của riêng bạn?

[Nâng cấp lên Premium](https://x.com/i/premium_sign_up)

[13:18 · 22 tháng 5 năm 2026](https://x.com/AnatoliKopadze/status/2057813254617858078)

·

[2,6 triệu lượt xem](https://x.com/AnatoliKopadze/status/2057813254617858078/analytics)

36

200

991

4,7K

Đọc 36 câu trả lời

## Mới sử dụng X?

Đăng ký với Apple

[Tạo tài khoản](https://x.com/i/flow/signup)

Bằng việc đăng ký, bạn đồng ý với [Điều khoản dịch vụ](https://x.com/tos) và [Chính sách bảo mật](https://x.com/privacy), bao gồm [Sử dụng cookie.](https://help.x.com/rules-and-policies/twitter-cookies)

## Những người có liên quan

*     [![Image 11](https://pbs.twimg.com/profile_images/1634313760444751873/QfwY91Hp_normal.jpg)](https://x.com/AnatoliKopadze) [Anatoli Kopadze](https://x.com/AnatoliKopadze) [@AnatoliKopadze](https://x.com/AnatoliKopadze) Theo dõi Nhấp để theo dõi AnatoliKopadze Thích nghi hoặc chết

# Đang thịnh hành

## Chuyện gì đang xảy ra vậy

Đang thịnh hành ở Pháp

Bennacer

Đang thịnh hành ở Pháp

Augustinô

Đang thịnh hành ở Pháp

tàu tấn công biển

Thể thao · Thịnh hành

Medvedev

[Hiển thị thêm](https://x.com/explore/tabs/for-you)

[Điều khoản dịch vụ](https://x.com/tos)

|

[Chính sách bảo mật](https://x.com/privacy)

|

[Chính sách cookie](https://support.x.com/articles/20170514)

|

[Khả năng tiếp cận](https://help.x.com/resources/accessibility)

|

|

Hơn

© 2026 X Corp.
