---
title: "Pinterest xây dựng MCP Ecosystem trong production như thế nào"
category: "AI Notes"
categoryOrder: 3
order: 1
source: "https://blog.bytebytego.com/p/how-pinterest-built-a-production"
sourceLabel: "ByteByteGo"
---

*Đây là tóm tắt và ghi chú cá nhân từ bài viết gốc trên ByteByteGo.*

## Vấn đề cốt lõi

Pinterest có hàng chục hệ thống nội bộ (Presto, Spark, Airflow, ticketing...). Khi muốn tích hợp AI agents vào, họ đối mặt với bài toán **N × M**:

- 5 AI surfaces × 10 internal tools = **50 custom integrations** cần xây và maintain

Model Context Protocol (MCP) giải quyết điều này bằng cách biến N × M thành **N + M**:
- Xây 1 MCP client/surface + 1 MCP server/tool
- Mọi client đều nói chuyện được với mọi server

## Những gì Pinterest phải xây ngoài protocol

Implement MCP chỉ là phần dễ. Phần khó là hệ sinh thái xung quanh:

**1. Central Registry**
Nơi đăng ký tất cả MCP servers, giúp AI agents tìm thấy tool cần dùng.

**2. Two-layer Auth**
- Layer 1: xác thực agent có quyền gọi MCP server không
- Layer 2: xác thực MCP server có quyền truy cập data source không

**3. Unified Deployment Pipeline**
Chuẩn hoá cách deploy và update MCP servers.

**4. Observability từ ngày đầu**
Logging, tracing, alerting được baked in — không phải add sau.

## Bài học rút ra

> "Implementing the protocol turned out to be the easy part."

Khi scale AI agents trong tổ chức lớn, infrastructure xung quanh (auth, registry, observability) quan trọng hơn bản thân protocol.

---

*Ghi chú cá nhân: MCP đang trở thành standard de facto cho AI tool integration. Đáng để theo dõi adoption trong các công ty VN.*
