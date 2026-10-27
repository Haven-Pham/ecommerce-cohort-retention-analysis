# 📊 Phân tích Cohort, Giữ chân Khách hàng & Lợi nhuận Thương mại Điện tử

[![English](https://img.shields.io/badge/Read-English-1D6AE5?style=flat-square)](README.md)
[![Portfolio](https://img.shields.io/badge/Portfolio-haven--portfolio02-0EA5E9?style=flat-square&logo=vercel&logoColor=white)](https://haven-portfolio02.vercel.app/?scroll=projects)

> **Tóm tắt:** Năm 2023 doanh thu tăng **+24%** nhưng lợi nhuận giảm **−12%** do biên lợi nhuận toàn danh mục giảm từ 18,0% xuống 12,8%. Khách mua lặp lại (31% tổng số khách) tạo ra **56% lợi nhuận**, nhưng thời gian trung vị đến lần mua thứ hai là **364 ngày**, và các khoản giảm giá trên 20% đã làm mất **289 nghìn USD**.

![Doanh thu, lợi nhuận và biên lợi nhuận](reports/figures/01_yearly_sales_profit_margin.png)

## 🎯 1. Bối cảnh & mục tiêu

Một nhà bán lẻ thương mại điện tử toàn cầu kinh doanh mỹ phẩm và đồ gia dụng (dữ liệu giả lập phục vụ học tập: **51.290 dòng đơn hàng**, **17.415 khách hàng**, 2020–2023) tăng trưởng đều mỗi năm. Ban lãnh đạo muốn biết tăng trưởng đó có dựa trên khách hàng quay lại hay không, và có tạo ra lợi nhuận hay không.

**Câu hỏi kinh doanh**
* 🔁 **Giữ chân:** bao nhiêu khách mới quay lại, và khi nào?
* 👥 **Phân khúc:** khách Consumer, Corporate và Self-Employed có hành vi khác nhau không?
* 💰 **Giá trị:** lợi nhuận phụ thuộc bao nhiêu vào khách mua lặp lại?
* 🏷️ **Động lực lợi nhuận:** nhóm khách và chính sách giá nào tạo ra hay làm mất lợi nhuận?

## 💻 2. Công cụ sử dụng

* **Python** 🐍: `pandas`, `numpy` (xây dựng cohort), `matplotlib`, `seaborn` (heatmap, biểu đồ)
* **Package tái sử dụng** `src/cohort_analysis/`: kiểm tra dữ liệu, hàm cohort và retention, phân tích lợi nhuận, style biểu đồ
* **Báo cáo:** `openpyxl` (báo cáo Excel), `python-pptx` (slide cho ban điều hành), Jupyter Notebook 📓
* **Chất lượng:** unit test `pytest` và GitHub Actions tự chạy lại toàn bộ notebook mỗi lần push

## 💡 3. Insight chính

### 📉 3.1 Tăng trưởng nhưng không có lãi trong năm 2023
* Doanh thu **1,77 → 2,19 triệu USD (+24%)**, lợi nhuận **319 → 280 nghìn USD (−12%)**; biên lợi nhuận **18,0% → 12,8%**, tương đương khoảng **115 nghìn USD** ở quy mô 2023.
* **Không phải do giảm giá:** đơn không giảm giá cũng giảm biên từ 33,4% xuống 28,1%, trong khi cơ cấu giảm giá không đổi.
* **Không phải do cơ cấu sản phẩm:** mọi ngành hàng đều mất 4–8 điểm % biên lợi nhuận trong khi tỷ trọng ngành hàng thay đổi dưới 1 điểm %. Điều này cho thấy **giá vốn hoặc giá bán đã thay đổi trên toàn công ty**.

### 🔁 3.2 Giữ chân: phần lớn khách không quay lại
* Chỉ **1,6%–2,4%** khách của một cohort mua lại trong bất kỳ tháng nào sau đó; theo quý là **2,7%–8,9%**.
* Không có đường suy giảm dần: số ít khách quay lại thì quay lại chậm và không đều.

### 💎 3.3 Khách mua lặp lại gánh lợi nhuận
* **31%** khách mua từ 2 lần trở lên tạo ra **56% lợi nhuận**: **110,6 USD**/khách so với **38,8 USD** của khách mua một lần.
* Thời gian trung vị đến lần mua thứ hai là **364 ngày**; chỉ **14,5%** quay lại trong 90 ngày. Điều này gợi ý chu kỳ mua theo năm hoặc theo nhu cầu bổ sung hàng.

### 🏷️ 3.4 Giảm giá sâu làm mất giá trị
* Các dòng giảm giá trên 20% (22% số dòng) có biên **−8%** và **−27%**, tổng lỗ **288,6 nghìn USD**.

### 👥 3.5 Phân khúc và thu nhập
* **Corporate:** 30% số khách nhưng chiếm **59% doanh thu, 57% lợi nhuận**; mức giữ chân tương đương các phân khúc khác.
* **Thu nhập không tạo khác biệt:** tỷ trọng lợi nhuận của mỗi nhóm thu nhập gần bằng tỷ trọng số khách (lợi nhuận mỗi khách 54–62 USD).

## 🚀 4. Khuyến nghị

| # | Hành động | Phụ trách | Tác động ước tính |
|---|---|---|---|
| 1 | Làm rõ nguyên nhân giảm biên 2023 bằng dữ liệu giá vốn và giá niêm yết trước khi đặt mục tiêu 2024 | Tài chính · Mua hàng | Tối đa ≈ 115 nghìn USD/năm |
| 2 | Giới hạn giảm giá ở 20%; trên mức này cần phê duyệt và kiểm tra biên | Kinh doanh | Tối đa ≈ 72 nghìn USD/năm |
| 3 | Chương trình mua lần hai vào tháng 10–12, kèm thử nghiệm A/B nhắc nhở sau 60–90 ngày | CRM · Marketing | +5% chuyển đổi mua lặp ≈ +43 nghìn USD |
| 4 | Quản lý tài khoản cho khách Corporate (nhịp đặt hàng lại, giá theo sản lượng thay vì giảm giá sâu) | Bán hàng | Bảo vệ 57% lợi nhuận |
| 5 | Thay nhắm mục tiêu theo thu nhập bằng phân khúc RFM và mức nhạy cảm với giảm giá | Phân tích marketing | Nhắm mục tiêu tốt hơn, không tốn thêm chi phí |

## 📦 5. Sản phẩm bàn giao

* [`notebooks/cohort_retention_profitability.ipynb`](notebooks/cohort_retention_profitability.ipynb): toàn bộ phân tích kèm kết quả
* [`reports/Cohort_Retention_Executive_Deck.pdf`](reports/Cohort_Retention_Executive_Deck.pdf): 8 slide cho ban điều hành (kèm `.pptx`)
* [`reports/Cohort_Retention_Profitability_Report.xlsx`](reports/Cohort_Retention_Profitability_Report.xlsx): bảng KPI, ma trận retention, phân khúc, giảm giá
* [`reports/figures/`](reports/figures) · [`reports/tables/`](reports/tables): biểu đồ (PNG) và bảng kết quả (CSV)

Cấu trúc thư mục, cách chạy và giới hạn của phân tích: xem [README tiếng Anh](README.md#️-6-repository-structure).

---
*Dự án thực hiện bởi **Phạm Hồng Hiếu (Haven)**, chuyên viên phân tích chuỗi cung ứng & dữ liệu · [Portfolio](https://haven-portfolio02.vercel.app) · [GitHub](https://github.com/Haven-Pham)* 🖋️
