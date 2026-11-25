# K5 Day 14: Instructor Slides (React)

Deck giảng viên **Deployment, Benchmark & Observability**: đưa agent từ laptop lên cloud, đạt `PASS 12/12`, rồi đo tốc độ và độ đúng. Cùng khung với deck Day 13 ([minhhai203/k5-day13-instructor-slides](https://github.com/minhhai203/k5-day13-instructor-slides)): Vite + React, timer theo checkpoint, ghi chú giảng viên, tự chọn lớp sáng/chiều.

Nội dung lấy từ repo lab [VinUni-AI20k/K5-L3-Day14-Deployment-Agent-Benchmark-Observability](https://github.com/VinUni-AI20k/K5-L3-Day14-Deployment-Agent-Benchmark-Observability), nhánh `main` sau PR #1 (format skeleton-lab): README (mục Lưu ý K5), RULES, CHECKPOINTS, SUBMISSION, RUBRIC, `06-lab-complete/README.md`. Deck không ghi số đo mẫu (MB, latency, accuracy): học viên tự đo.

## Live

https://minhhai203.github.io/k5-day14-instructor-slides/ (thêm `?ca=sang` hoặc `?ca=chieu` để chọn ca)

## Sửa nội dung

```bash
python3 -I content/build_content.py
```

## Dev và build

```bash
cd app
npm install
npm run dev
npm run build   # output: app/dist, base path /k5-day14-instructor-slides/
# deploy: copy app/dist/ vào minhhai203.github.io/k5-day14-instructor-slides/ rồi push
```

## Lớp sáng và lớp chiều

Slide viết theo giờ lớp chiều (14:00 đến 18:00), lấy từ bảng giờ tương đối 0:00 → 4:00 trong CHECKPOINTS.md của lab. Mở deck trước 13:00 là lớp sáng (09:00 đến 13:00): mọi mốc giờ dời sớm 5 tiếng. Hạn nộp của cả hai lớp: 23h59 GMT+7 ngày lab. Đổi ở `app/src/session.ts`.

## Phím tắt

| Phím | Việc |
|------|------|
| ← → / Space | Đổi slide |
| P / R | Dừng hoặc chạy timer / đặt lại |
| M | Âm báo |
| B | Nhạc nền |
| N | Ghi chú giảng viên |
| F | Toàn màn hình |

Timer tự chạy khi mở slide checkpoint: CP0 10 phút, CP1 20, CP2 30, CP3 25, CP4 20, CP5 60, CP6 25, CP7 45. CP8 làm sau giờ lab, không có timer.

## Lưu ý

Link deck là công khai.
