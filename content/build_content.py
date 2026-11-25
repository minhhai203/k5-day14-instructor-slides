"""Builds app/src/slides/content.json for the Day 14 instructor deck.

Same frame as the Day 13 deck (minhhai203/k5-day13-instructor-slides): opening, format, schedule,
naming, rules, K5 notes, one slide per checkpoint (meta bar, task, "Cách làm", anti-pattern,
self-check), rubric and the submission checklist.

Facts come from the Day 14 lab repo VinUni-AI20k/K5-L3-Day14-Deployment-Agent-Benchmark-Observability,
branch main after PR #1 (skeleton-lab format): README.md (section "Lưu ý khi làm bài (K5)"),
RULES.md, CHECKPOINTS.md, SUBMISSION.md, RUBRIC.md, 06-lab-complete/README.md.
The deck states no measured number (image size, latency, accuracy): students measure their own.

Slide times are afternoon clock times (14:00 to 18:00); the app shifts them for the morning class
(app/src/session.ts).

Run from the repo root:  python3 -I content/build_content.py
"""
import json
import pathlib

ICONS = json.loads((pathlib.Path(__file__).resolve().parent / "icons.json").read_text())

S = []


def slide(title, html, notes, cp=None, minutes=None, label=None, done=None):
    S.append({
        "index": len(S),
        "title": title,
        "html": html.strip().replace("{ICONS_ANTI}", ICONS["anti"]),
        "notes": notes.strip(),
        "activeCp": cp,
        "timerMin": minutes,
        "timerLabel": label,
        "completedThrough": done,
    })


def meta(**rows):
    names = {
        "when": "Giờ",
        "where": "Thư mục",
        "write": "Ghi vào",
        "out": "Sản phẩm",
    }
    body = "".join(f"<div><dt>{names[k]}</dt><dd>{v}</dd></div>" for k, v in rows.items())
    return f'<dl class="meta">{body}</dl>'


def coach(*items):
    """Student-facing "Cách làm" box. The deck is projected to students, so every item is shown in full."""
    li = "".join(f"<li>{x}</li>" for x in items)
    return f'<section class="coach"><h3>{ICONS["coach"]}Cách làm</h3><ul>{li}</ul></section>'


def anti(*items):
    li = "".join(f"<li>{x}</li>" for x in items)
    return f'<section class="anti"><h3>{ICONS["anti"]}Lỗi thường gặp</h3><ul>{li}</ul></section>'


def check(text):
    return f'<section class="selfcheck"><h3>{ICONS["check"]}Tự kiểm tra</h3><p>{text}</p></section>'


def notes(title, *items):
    li = "".join(f"<li>{x}</li>" for x in items)
    return f"<strong>{title}</strong>\n<ul>{li}</ul>"


# Writing rules (same as Day 13): one sentence = one idea, instructions start with the verb,
# keep code, commands, paths, ports and times unchanged. Talk to the student, not about the docs.

REPO = "https://github.com/VinUni-AI20k/K5-L3-Day14-Deployment-Agent-Benchmark-Observability"

# 0 ── Title ─────────────────────────────────────────────────────────────
slide(
    "Day 14: Deployment, Benchmark & Observability",
    """
<div class="title-slide">
  <div class="title-copy">
    <p class="course"><b>Day 14 · Deployment, Benchmark &amp; Observability</b> · VinUni AI20k, K5 Level 3 (3A và 3B), {{SESSION}}, {{SESSION_RANGE}}</p>
    <h1 class="hero">Đưa agent lên cloud. Đo nó. Giám sát nó.</h1>
    <p class="lede">Bắt đầu từ một agent chỉ chạy được trên laptop. Kết thúc với một agent có URL public, đạt 12/12 tiêu chí production, có số đo tốc độ và độ đúng của chính bạn.</p>
  </div>
  <figure class="title-proof">
    <figcaption>Mốc phải đạt trong buổi:</figcaption>
<pre class="code code--big"><span class="c"># CP5 · 06-lab-complete/</span>
python check_production_ready.py
  → PASS 12/12
<span class="c"># CP6 · URL public</span>
/health 200 · /ask không key 401</pre>
  </figure>
</div>
<div class="facts">
  <section><h2>Hình thức</h2><p>Bài cá nhân. 4 giờ tại lớp. Mock LLM, không cần API key LLM.</p></section>
  <section><h2>Chấm điểm</h2><p>Bài tối đa 120 điểm, đổi về thang 100. Cần 70/100 để qua.</p></section>
  <section><h2>Hạn nộp</h2><p>{{DEADLINE}} (GMT+7).</p></section>
  <section><h2>Phím</h2><p><kbd>←</kbd> <kbd>→</kbd>: đổi slide. <kbd>N</kbd>: ghi chú.</p></section>
</div>
""",
    notes(
        "Mở đầu buổi học",
        "Hỏi lớp: “Agent của bạn chạy được trên laptop. Vậy đã đưa cho người khác dùng được chưa?”",
        "Nói: hôm nay đi đủ đường từ laptop tới cloud, rồi đo xem agent nhanh và đúng tới đâu.",
        "Phần nặng điểm nhất là Part 6 (60/120). Không để Part 1–5 lấn sang giờ của Part 6.",
        "Mọi số trong bài (MB, latency, accuracy) phải là số học viên tự đo.",
    ),
)

# 1 ── Journey ───────────────────────────────────────────────────────────
slide(
    "Bảy phần, một agent",
    """
<h2 class="title">Bảy phần của lab, gộp lại thành một agent production</h2>
<ol class="loop loop--flow">
  <li><b>Part 1 · Localhost</b><span>Tìm anti-pattern trong code chạy trên laptop</span></li>
  <li><b>Part 2 · Docker</b><span>Image multi-stage, đo số MB</span></li>
  <li><b>Part 4 · Security</b><span>API key, rate limit 429, cost guard</span></li>
  <li><b>Part 5 · Scaling</b><span>/health, /ready, stateless với Redis</span></li>
  <li><b>Part 6 · Final</b><span>Sửa TODO tới khi PASS 12/12</span></li>
  <li><b>Part 3 · Deploy</b><span>Đưa agent Part 6 lên Railway hoặc Render</span></li>
  <li><b>Part 7 · Đo</b><span>Load test, eval, Grafana, Jaeger, alert</span></li>
</ol>
<div class="grid grid-2">
  <section class="panel">
    <h3>Lớp K5 làm khác <code>CODE_LAB.md</code> ở ba điểm</h3>
    <ul class="plain">
      <li>Part 1, 2, 4, 5: chạy ví dụ có sẵn, trả lời vào <code>MISSION_ANSWERS.md</code>.</li>
      <li>Part 3 làm sau Part 6. Deploy luôn agent Part 6, không deploy app mẫu.</li>
      <li>Part 7 Bước 1 làm tại lớp. Bước 2 (Docker stack) làm sau giờ lab.</li>
    </ul>
  </section>
  <section class="panel panel--do">
    <h3>Đọc theo thứ tự</h3>
    <p>README → RULES → CHECKPOINTS → SUBMISSION → RUBRIC.</p>
    <p class="cp-ref">Mục “⚠️ Lưu ý khi làm bài (K5)” trong README sửa các lệnh trong <code>CODE_LAB.md</code> chạy không đúng.</p>
  </section>
</div>
""",
    notes(
        "Vì sao đổi thứ tự",
        "Lộ trình trong <code>CODE_LAB.md</code> dài 335 phút. Lớp có 240 phút.",
        "Deploy app mẫu rồi deploy lại agent Part 6 là làm hai lần. Lớp K5 chỉ deploy một lần, ở CP6.",
        "Part 7 Bước 2 cần Docker stack nặng (Prometheus, Grafana, Jaeger, Locust). Làm ở nhà, trước hạn nộp.",
    ),
)

# 2 ── Schedule ──────────────────────────────────────────────────────────
slide(
    "Chín checkpoint và mốc giờ",
    """
<h2 class="title">Chín checkpoint và giờ bắt đầu</h2>
<table class="data data--compact">
  <thead><tr><th>Giờ</th><th>Checkpoint</th><th>Phần trong <code>CODE_LAB.md</code></th><th>Phút</th></tr></thead>
  <tbody>
    <tr><td class="num">14:00</td><td><b>CP0</b> Setup</td><td>Fork, đổi tên repo, kiểm Python + Docker</td><td class="num">10</td></tr>
    <tr><td class="num">14:10</td><td><b>CP1</b> Localhost vs Production</td><td>Part 1 (1.1–1.3)</td><td class="num">20</td></tr>
    <tr><td class="num">14:30</td><td><b>CP2</b> Docker</td><td>Part 2 (2.1–2.4)</td><td class="num">30</td></tr>
    <tr><td class="num">15:00</td><td><b>CP3</b> API Security</td><td>Part 4 (4.1–4.4)</td><td class="num">25</td></tr>
    <tr><td class="num">15:25</td><td><b>CP4</b> Scaling &amp; Reliability</td><td>Part 5 (5.1–5.5)</td><td class="num">20</td></tr>
    <tr><td class="num">15:45</td><td>Nghỉ</td><td></td><td class="num">5</td></tr>
    <tr class="row-key"><td class="num">15:50</td><td><b>CP5</b> Final Project</td><td>Part 6 → <code>PASS 12/12</code></td><td class="num">60</td></tr>
    <tr><td class="num">16:50</td><td><b>CP6</b> Cloud Deployment</td><td>Part 3, deploy agent Part 6</td><td class="num">25</td></tr>
    <tr><td class="num">17:15</td><td><b>CP7</b> Benchmark local</td><td>Part 7 Bước 1 (7.1–7.3)</td><td class="num">45</td></tr>
    <tr><td class="num">Sau lab</td><td><b>CP8</b> Observability + nộp</td><td>Part 7 Bước 2 (7.4–7.7)</td><td class="num">tới hạn</td></tr>
  </tbody>
</table>
<p class="note">Kẹt quá 10 phút ở một mốc: gọi Lab Coach, ghi lại lỗi, rồi đi tiếp mốc sau. Hạn nộp link LMS: {{DEADLINE}}.</p>
""",
    notes(
        "Giờ trong buổi",
        "Giờ lấy từ bảng trong CHECKPOINTS.md (0:00 → 4:00), viết theo lớp chiều 14:00–18:00.",
        "Lớp sáng dùng cùng lịch, sớm hơn 5 tiếng. Deck tự chọn ca theo giờ máy. Nút trên header đổi ca bằng tay.",
        "Mốc cứng nhất: 15:50. Ai chưa xong CP1–CP4 vẫn chuyển sang CP5, phần còn lại làm sau.",
        "Timer tự chạy khi mở slide checkpoint.",
    ),
)

# 3 ── Repo naming ───────────────────────────────────────────────────────
slide(
    "Tạo repo bài làm và đặt tên",
    f"""
<h2 class="title">Tạo repo bài làm. Đặt tên đúng từ đầu.</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>Tên repo (bài cá nhân)</h3>
<pre class="code code--wrap">K5-L3A-DAY14-HoVaTen-MSSV-Deployment-Benchmark-Observability
K5-L3B-DAY14-HoVaTen-MSSV-Deployment-Benchmark-Observability</pre>
    <p>Họ tên viết liền, không dấu, viết hoa chữ cái đầu. Ví dụ: <code>K5-L3A-DAY14-NguyenVanA-2A2026xxxxx-Deployment-Benchmark-Observability</code>.</p>
    <h3>Ba bước</h3>
    <ol class="plain">
      <li>Fork repo đề bài về tài khoản cá nhân.</li>
      <li><b>Settings → Repository name</b>: đổi tên theo mẫu.</li>
      <li>Clone bản fork. Làm bài trong bản fork.</li>
    </ol>
<pre class="code code--wrap">{REPO}</pre>
  </section>
  <div class="stack">
    <section class="panel">
      <h3>Nộp bài</h3>
      <p>Nộp <b>link repo</b> trên LMS. Repo để <b>Public</b>. Không nộp file zip.</p>
      <p>Bản được chấm: commit cuối trước hạn nộp.</p>
    </section>
    <section class="anti">
      <h3>{{ICONS_ANTI}}Lỗi thường gặp</h3>
      <ul>
        <li>Làm trên repo đề bài, không phải bản fork.</li>
        <li>Để repo Private: Lab Coach không mở được thì không chấm.</li>
        <li>Copy code Part 6 ra ngoài <code>06-lab-complete/</code>.</li>
      </ul>
    </section>
  </div>
</div>
""",
    notes(
        "Việc của coach trong 10 phút đầu",
        "Quy tắc tên lấy từ SUBMISSION.md. Sai tên mà vẫn tìm được bài: −5 điểm.",
        "Mở link repo ở cửa sổ ẩn danh để kiểm Public.",
        "Cây thư mục <code>app/</code> ở gốc repo trong <code>DAY14_DELIVERY_CHECKLIST.md</code> không áp dụng cho K5. Code Part 6 nằm trong <code>06-lab-complete/</code>.",
    ),
)

# 4 ── Rules ─────────────────────────────────────────────────────────────
slide(
    "Luật làm bài",
    """
<h2 class="title">Luật làm bài</h2>
<table class="data data--compact">
  <thead><tr><th>Phần</th><th>Làm</th><th>Không làm</th></tr></thead>
  <tbody>
    <tr><td class="num">AI</td><td>Hỏi khái niệm, đọc lỗi, gợi ý cách sửa. Ghi mục <b>AI log</b> cuối <code>MISSION_ANSWERS.md</code>.</td><td>Bịa số đo: MB, latency, accuracy, thời gian alert.</td></tr>
    <tr><td class="num">Script chấm</td><td>Chạy <code>check_production_ready.py</code> nhiều lần.</td><td>Sửa <code>check_production_ready.py</code>: Part 6 = 0 điểm.</td></tr>
    <tr><td class="num">Eval</td><td>Sửa <code>KNOWLEDGE_BASE</code> trong <code>mock_llm.py</code>.</td><td>Sửa <code>golden_dataset.jsonl</code>.</td></tr>
    <tr><td class="num">Secret</td><td>Đặt <code>AGENT_API_KEY</code> bằng biến môi trường. Chỉ commit <code>.env.example</code>.</td><td>Commit <code>.env</code>, key, token Railway/Render: −10 điểm.</td></tr>
    <tr><td class="num">Sao chép</td><td>Thảo luận với bạn.</td><td>Dùng chung URL deploy, ảnh dashboard, file report.</td></tr>
    <tr><td class="num">Thông tin cá nhân</td><td>Ghi họ tên, MSSV ở tên repo và ô Họ tên của <code>BENCHMARK_REPORT.md</code>.</td><td>Ghi email, số điện thoại vào bài.</td></tr>
  </tbody>
</table>
<p class="note">Lỡ commit secret: đổi key mới ngay trên dashboard, rồi báo Lab Coach. Xoá file thôi chưa đủ, vì secret vẫn nằm trong lịch sử git.</p>
""",
    notes(
        "Nói rõ với lớp (RULES.md)",
        "Lab Coach có thể yêu cầu giải thích bất kỳ đoạn code nào trong <code>06-lab-complete/app/</code> hoặc bất kỳ số nào trong báo cáo.",
        "Số trong <code>BENCHMARK_REPORT.md</code> không khớp file JSON/CSV: mục Part 7 đó 0 điểm.",
        "Dùng gói miễn phí hoặc dùng thử của Railway/Render. Nền tảng đòi thẻ mà học viên không muốn nhập: báo Lab Coach.",
        "Xong lab thì tắt stack Docker: <code>docker compose -p &lt;tên&gt; down -v</code>.",
    ),
)

# 5 ── K5 notes ──────────────────────────────────────────────────────────
slide(
    "Lưu ý K5 trước khi bắt đầu",
    """
<h2 class="title">Lưu ý K5: đọc trước khi chạy lệnh</h2>
<p class="lede">Đủ 11 ý nằm trong mục “⚠️ Lưu ý khi làm bài (K5)” của README.</p>
<div class="grid grid-2">
  <section class="panel">
    <h3>Máy và môi trường</h3>
    <ul class="plain">
      <li><b>Windows:</b> chạy Python trong WSL2. <code>python -c "import os; print(os.name)"</code> phải in <code>posix</code>. Python Windows không gửi được SIGTERM, nên không bao giờ đạt 12/12.</li>
      <li><b>Cổng 8000:</b> tắt server cũ trước khi bật bản mới.</li>
      <li><b>Compose Part 2, Part 5:</b> chạy <code>touch .env.local</code> trong thư mục đó trước.</li>
      <li><b>Ba thư mục tên <code>production</code>:</b> luôn dùng <code>-p</code> và <code>--build</code> như lệnh trên slide.</li>
    </ul>
  </section>
  <section class="panel">
    <h3>Lệnh khác <code>CODE_LAB.md</code></h3>
    <ul class="plain">
      <li><b>Part 1–2:</b> <code>curl -X POST "http://localhost:8000/ask?question=Hello"</code>. Gửi JSON sẽ ra 422.</li>
      <li><b>Part 2:</b> build từ gốc repo: <code>docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .</code></li>
      <li><b>Part 4:</b> token ở <code>POST /auth/token</code>, tài khoản <code>student</code> / <code>demo123</code>.</li>
      <li><b>Part 5:</b> cổng <b>8080</b>, endpoint <b><code>POST /chat</code></b>.</li>
      <li><b>Part 7:</b> <code>load_test.py</code>, <code>run_eval.py</code> chỉ ghi file khi có <code>--out</code>.</li>
    </ul>
  </section>
</div>
""",
    notes(
        "Vì sao có slide này",
        "Mục Lưu ý trong README có 11 ý. Slide gom các ý gây kẹt nhiều nhất.",
        "Gặp lỗi 422, 404, 405, thiếu <code>.env.local</code> hay cổng bận: chỉ học viên về đúng số trong mục Lưu ý.",
        "Hỏi lớp ngay ở CP0: ai dùng Windows? Kiểm WSL2 trước, đừng đợi tới CP5.",
    ),
)

# 6 ── CP0 ───────────────────────────────────────────────────────────────
slide(
    "CP0: Setup",
    f"""
<h2 class="title">CP0: repo đúng tên, máy có Python và Docker</h2>
{meta(when="14:00–14:10", where="Gốc repo bản fork", out="Repo đã đổi tên, clone về máy")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap">git clone &lt;URL_BAN_FORK&gt;
cd &lt;TEN_REPO&gt;
python --version            <span class="c"># 3.11 trở lên</span>
docker compose version
docker run --rm hello-world
python -c "import os; print(os.name)"   <span class="c"># Windows: phải in posix</span></pre>
    <section class="panel">
      <h3>Chuẩn bị trước cho CP6</h3>
      <p>Tạo tài khoản Railway hoặc Render. Railway CLI cài bằng <code>npm</code>, cần Node.js.</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Fork, đổi tên, rồi mới clone.",
        "Đọc mục <i>Lưu ý khi làm bài</i> trong README.",
        "Không có Docker vẫn làm được CP1, CP3, CP7. CP2, CP5 và CP8 cần Docker: báo Lab Coach ngay.",
    )}
    {anti(
        "Clone repo đề bài thay vì bản fork.",
        "Docker Desktop chưa bật.",
        "Windows: chạy trong PowerShell hoặc Git Bash thay vì WSL2.",
    )}
    {check("<code>docker run --rm hello-world</code> chạy được chưa? Tên repo trên GitHub đã đúng mẫu chưa?")}
  </div>
</div>
""",
    notes(
        "Việc của coach trong CP0",
        "Đi một vòng lớp: ai chưa có Docker, ai dùng Windows không có WSL2.",
        "Part 7 Bước 2 chạy 6 container. Nhắc học viên đóng ứng dụng nặng.",
        "Học viên không có Docker: cho làm CP1, CP3, CP7 trước, ghép máy bạn để xem CP2.",
    ),
    cp="0",
    minutes=10,
    label="CP0 · Setup",
)

# 7 ── CP1 ───────────────────────────────────────────────────────────────
slide(
    "CP1: Localhost vs Production",
    f"""
<h2 class="title">CP1: code chạy trên laptop còn thiếu gì</h2>
{meta(when="14:10–14:30", where="<code>01-localhost-vs-production/</code>", write="<code>MISSION_ANSWERS.md</code> mục Part 1", out="≥ 5 anti-pattern, bảng so sánh develop/production")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap">cd 01-localhost-vs-production/develop
pip install -r requirements.txt
python app.py
<span class="c"># terminal khác: question đi qua query, không qua JSON</span>
curl -X POST "http://localhost:8000/ask?question=Hello"</pre>
    <section class="panel">
      <h3>Exercise 1.1–1.3</h3>
      <ul class="plain">
        <li>1.1: đọc <code>develop/app.py</code>, tìm ít nhất 5 anti-pattern.</li>
        <li>1.2: chạy bản develop, gọi thử.</li>
        <li>1.3: bảng so sánh develop/production, có cột “vì sao quan trọng”.</li>
      </ul>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Mỗi anti-pattern ghi kèm dòng code trong <code>develop/app.py</code>.",
        "Đặt cạnh <code>production/app.py</code> để thấy bản đã sửa.",
        "Tắt server bằng Ctrl+C trước khi sang bản production (cùng cổng 8000).",
    )}
    {anti(
        "Gửi body JSON cho bản develop: ra 422.",
        "Liệt kê anti-pattern mà không chỉ ra dòng code.",
    )}
    {check("Chỉ ra được một anti-pattern trong <code>develop/app.py</code> mà <code>production/app.py</code> đã sửa, kèm dòng code?")}
  </div>
</div>
""",
    notes(
        "Câu hỏi gợi ý",
        "“Vì sao hardcode secret nguy hiểm, kể cả trong repo private?”",
        "“Nếu không có health check, nền tảng cloud biết app chết bằng cách nào?”",
        "Không để học viên viết lại code mẫu. Chỉ chạy và trả lời.",
    ),
    cp="1",
    minutes=20,
    label="CP1 · Localhost",
)

# 8 ── CP2 ───────────────────────────────────────────────────────────────
slide(
    "CP2: Docker",
    f"""
<h2 class="title">CP2: đóng gói agent thành image nhỏ</h2>
{meta(when="14:30–15:00", where="Gốc repo, <code>02-docker/</code>", write="<code>MISSION_ANSWERS.md</code> mục Part 2", out="Số MB tự đo, % chênh, sơ đồ stack")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># build từ GỐC repo, không cd vào thư mục con</span>
docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .
docker build -f 02-docker/production/Dockerfile -t my-agent:advanced .
docker images | grep my-agent

<span class="c"># Exercise 2.4</span>
cd 02-docker/production &amp;&amp; touch .env.local
docker compose up</pre>
    <section class="panel">
      <h3>Phải có trong bài</h3>
      <p>4 câu trả lời 2.1 · kết quả gọi container · kích thước hai image và % chênh · sơ đồ service của stack 2.4 · kết quả test qua Nginx.</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Đọc Dockerfile develop trước, trả lời 4 câu 2.1.",
        "Ghi số MB từ <code>docker images</code> trên máy bạn.",
        "Xong 2.4 thì <code>docker compose down</code> để trả cổng.",
    )}
    {anti(
        "<code>cd 02-docker/develop</code> rồi build: lỗi <code>COPY</code> không thấy file.",
        "Quên <code>touch .env.local</code>: compose báo thiếu file.",
        "Chép số MB từ README thay vì tự đo.",
    )}
    {check("Image production nhỏ hơn bao nhiêu phần trăm? Vì sao <code>COPY requirements.txt</code> đứng trước <code>COPY . .</code>?")}
  </div>
</div>
""",
    notes(
        "Việc của coach trong CP2",
        "Build lần đầu mất vài phút. Cho học viên đọc Dockerfile trong lúc chờ.",
        "Câu hỏi: “Multi-stage giảm dung lượng ở bước nào?” Stage build có compiler, stage runtime chỉ copy kết quả.",
        "Không chiếu số MB mẫu. Mỗi máy ra số khác nhau.",
    ),
    cp="2",
    minutes=30,
    label="CP2 · Docker",
)

# 9 ── CP3 ───────────────────────────────────────────────────────────────
slide(
    "CP3: API Security",
    f"""
<h2 class="title">CP3: API key, rate limit, cost guard</h2>
{meta(when="15:00–15:25", where="<code>04-api-gateway/</code>", write="<code>MISSION_ANSWERS.md</code> mục Part 4", out="Output <code>curl -i</code>: 401, 200, 429")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># 4.1 develop</span>
AGENT_API_KEY=secret-key-123 python app.py

<span class="c"># 4.2–4.3 production: tắt develop trước, cài requirements</span>
curl -X POST http://localhost:8000/auth/token \\
  -H "Content-Type: application/json" \\
  -d '{{"username":"student","password":"demo123"}}'
<span class="c"># dùng token đó cho vòng lặp 4.3, thêm -i để thấy mã HTTP</span></pre>
    <section class="panel">
      <h3>Rate limit khác cost guard</h3>
      <p>Rate limit chặn gọi quá nhanh → <b>429</b>. Cost guard chặn tiêu quá ngân sách → <b>402</b>. Cần cả hai.</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Thêm <code>-i</code> vào curl, dán cả dòng mã HTTP vào bài.",
        "4.2 không cần tự viết JWT, nhưng vẫn phải lấy token.",
        "Che token trước khi dán vào bài.",
    )}
    {anti(
        "Gọi <code>/token</code> với <code>admin</code>/<code>secret</code> như trong <code>CODE_LAB.md</code>: sai endpoint.",
        "Quên tắt bản develop: hai app tranh cổng 8000.",
    )}
    {check("Vòng lặp curl của chính bạn có ra 429 không? Tài khoản <code>student</code> giới hạn 10 request/phút.")}
  </div>
</div>
""",
    notes(
        "Câu hỏi gợi ý",
        "“Rate limit đếm theo gì? Theo IP, theo user hay theo API key?”",
        "“Vì sao state của rate limit phải nằm trong Redis khi chạy nhiều instance?” Câu này nối sang CP4.",
        "Mục Lưu ý số 6 trong README có đủ lệnh.",
    ),
    cp="3",
    minutes=25,
    label="CP3 · Security",
)

# 10 ── CP4 ──────────────────────────────────────────────────────────────
slide(
    "CP4: Scaling & Reliability",
    f"""
<h2 class="title">CP4: nhiều instance, không mất state</h2>
{meta(when="15:25–15:45", where="<code>05-scaling-reliability/</code>", write="<code>MISSION_ANSWERS.md</code> mục Part 5", out="Kết quả <code>test_stateless.py</code> và giải thích")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap">cd 05-scaling-reliability/production
touch .env.local
docker compose -p k5-day14-scaling up -d --build --scale agent=3
python test_stateless.py        <span class="c"># cổng 8080, POST /chat</span>
docker compose -p k5-day14-scaling down</pre>
    <section class="panel">
      <h3>Hai endpoint, hai câu hỏi</h3>
      <p><code>/health</code> (liveness): process còn sống không? <code>/ready</code> (readiness): đã nhận request được chưa, Redis có kết nối không?</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Dùng đúng <code>-p k5-day14-scaling</code> và <code>--build</code>.",
        "Script gửi 5 câu trong một session rồi đọc history. Script không tự tắt instance.",
        "Giải thích: vì sao history vẫn còn khi request rơi vào instance khác?",
    )}
    {anti(
        "Bỏ <code>-p</code>: compose dùng lại image <code>production-agent</code> của CP2.",
        "Gọi cổng 80 hoặc <code>/ask</code>: stack này dùng 8080 và <code>/chat</code>.",
    )}
    {check("Vì sao state lưu trong RAM sẽ hỏng khi chạy 3 instance sau load balancer?")}
  </div>
</div>
""",
    notes(
        "Trước giờ nghỉ",
        "15:45 nghỉ 5 phút. 15:50 cả lớp chuyển sang CP5, kể cả ai chưa xong CP1–CP4.",
        "Nhắc: <code>docker compose -p k5-day14-scaling down</code> trước khi sang CP5 để trả cổng và RAM.",
        "Câu hỏi: “<code>/health</code> có nên trả 503 khi Redis chết không?” Không. Đó là việc của <code>/ready</code>.",
    ),
    cp="4",
    minutes=20,
    label="CP4 · Scaling",
)

# 11 ── CP5 ──────────────────────────────────────────────────────────────
slide(
    "CP5: Final Project, PASS 12/12",
    f"""
<h2 class="title">CP5: sửa hết TODO tới khi PASS 12/12</h2>
{meta(when="15:50–16:50", where="<code>06-lab-complete/</code>", write="<code>MISSION_ANSWERS.md</code>: dán “📋 Checklist Deliverable”", out="<code>check_production_ready.py</code> báo PASS 12/12")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap">cd 06-lab-complete
python check_production_ready.py --static-only   <span class="c"># chạy sớm, chạy sau mỗi bước</span>
python check_production_ready.py --skip-docker   <span class="c"># nhanh, bỏ build image</span>
python check_production_ready.py                 <span class="c"># bản đầy đủ, cần Docker</span></pre>
    <section class="panel">
      <h3>Các file có TODO</h3>
      <p><code>app/config.py</code> · <code>auth.py</code> (401) · <code>rate_limiter.py</code> (429) · <code>cost_guard.py</code> (402) · <code>redis_client.py</code> · <code>main.py</code> · <code>Dockerfile</code> · <code>docker-compose.yml</code> · <code>.dockerignore</code> · <code>.env.example</code> · <code>railway.toml</code> hoặc <code>render.yaml</code></p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Làm theo thứ tự gợi ý trong <code>06-lab-complete/README.md</code>.",
        "Đọc mục <i>Script chấm dựa vào những tiêu chí dưới đây</i> trước khi viết code.",
        "Chạy bản đầy đủ trước khi sang CP6.",
    )}
    {anti(
        "Sửa <code>check_production_ready.py</code> để lấy PASS: Part 6 = 0.",
        "Tự đăng ký handler SIGTERM mà không gọi lại handler cũ: uvicorn không tắt.",
        "<code>/health</code> trả 503 khi Redis chết.",
    )}
    {check("Script có in <code>PASS 12/12</code> ở chế độ đầy đủ không? Mục ⚠️ cũng tính là chưa đạt.")}
  </div>
</div>
""",
    notes(
        "Việc của coach trong CP5",
        "Đây là 60/120 điểm. Đi từng bàn, xem output script chấm trước, rồi mới xem code.",
        "Hỏi học viên mục nào đang ❌, rồi chỉ về đúng dòng trong bảng ở slide sau.",
        "Windows không có WSL2: Graceful shutdown luôn ⚠️. Chuyển sang WSL2 ngay.",
        "Lần đầu chạy bản đầy đủ mất vài phút vì build image.",
    ),
    cp="5",
    minutes=60,
    label="CP5 · Final 12/12",
)

# 12 ── CP5 contract ─────────────────────────────────────────────────────
slide(
    "CP5: script chấm kiểm gì",
    """
<h2 class="title">CP5: script chấm kiểm những gì</h2>
<table class="data data--compact">
  <thead><tr><th>Hạng mục</th><th>Agent phải làm</th></tr></thead>
  <tbody>
    <tr><td class="num"><code>GET /health</code></td><td>Luôn 200 khi process còn chạy, kể cả khi Redis chưa kết nối.</td></tr>
    <tr><td class="num"><code>GET /ready</code></td><td>200 khi sẵn sàng. <b>503</b> khi Redis (<code>REDIS_URL</code>) không kết nối được.</td></tr>
    <tr><td class="num"><code>POST /ask</code></td><td>Body JSON <code>{"question": "..."}</code> → 200.</td></tr>
    <tr><td class="num">API key</td><td><code>X-API-Key</code> phải trùng <code>AGENT_API_KEY</code>. Thiếu hoặc sai → <b>401</b>.</td></tr>
    <tr><td class="num">Rate limit</td><td>Vượt <code>RATE_LIMIT_PER_MINUTE</code> / 60 giây mỗi key → <b>429</b>. State trong Redis.</td></tr>
    <tr><td class="num">Cost guard</td><td>Vượt <code>DAILY_BUDGET_USD</code> hoặc <code>MONTHLY_BUDGET_USD</code> → <b>402</b>.</td></tr>
    <tr><td class="num">Log</td><td>Mỗi dòng log của app là 1 JSON object hợp lệ.</td></tr>
    <tr><td class="num">Graceful shutdown</td><td>SIGTERM khi đang có request: request đó vẫn 200, process thoát với exit code 0. <code>docker stop</code> &lt; 10 giây.</td></tr>
    <tr class="row-key"><td class="num">Docker image</td><td>Multi-stage, base slim, non-root, có <code>HEALTHCHECK</code>, &lt; 500 MB, khởi động được khi không có Redis.</td></tr>
    <tr><td class="num">Compose · Deploy config</td><td>Agent + <code>redis:*</code>, <code>depends_on</code>. <code>railway.toml</code> hoặc <code>render.yaml</code> có health check <code>/health</code>.</td></tr>
  </tbody>
</table>
""",
    notes(
        "Dùng slide này khi học viên hỏi “script muốn gì”",
        "Nguồn: mục <i>Script chấm dựa vào những tiêu chí dưới đây</i> trong <code>06-lab-complete/README.md</code>. <code>CODE_LAB.md</code> gọi bảng này là “Bảng Hợp đồng”.",
        "Biến môi trường đọc từ env và liệt kê đủ trong <code>.env.example</code>. Script chạy với <code>ENVIRONMENT=staging</code>.",
        "<code>.dockerignore</code> phải loại <code>.env</code>, <code>__pycache__</code>, <code>venv</code>.",
    ),
    cp="5",
)

# 13 ── CP6 ──────────────────────────────────────────────────────────────
slide(
    "CP6: Cloud Deployment",
    f"""
<h2 class="title">CP6: deploy agent Part 6, có Redis và API key</h2>
{meta(when="16:50–17:15", where="<code>06-lab-complete/</code>", write="<code>DEPLOYMENT.md</code>, <code>MISSION_ANSWERS.md</code> mục Part 3", out="URL public, ảnh trong <code>screenshots/</code>")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># Railway (hoặc Render theo Exercise 3.2)</span>
cd 06-lab-complete &amp;&amp; railway up

<span class="c"># tự kiểm: mỗi lệnh chỉ in mã HTTP (đủ lệnh ở CP6 trong CHECKPOINTS.md)</span>
curl -sS -o /dev/null -w '%{{http_code}}\\n' "$BASE/health"   <span class="c"># 200</span>
curl -sS -o /dev/null -w '%{{http_code}}\\n' "$BASE/ready"    <span class="c"># 200</span>
<span class="c"># POST $BASE/ask không có key                           → 401</span>
<span class="c"># POST $BASE/ask có -H "X-API-Key: $AGENT_API_KEY"       → 200</span></pre>
    <section class="panel">
      <h3>Đủ 8 điểm Part 3 trên một nền tảng</h3>
      <p>Deploy (4) · so sánh <code>railway.toml</code> với <code>render.yaml</code> (3) · vài dòng về pipeline Cloud Run, Exercise 3.3 (1).</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Tạo Redis trên nền tảng. Đặt <code>REDIS_URL</code> của service agent trỏ tới nó.",
        "Đặt <code>AGENT_API_KEY</code> bằng biến môi trường trên nền tảng.",
        "Copy 4 lệnh tự kiểm từ CP6 trong CHECKPOINTS.md, không gõ tay.",
    )}
    {anti(
        "Deploy app mẫu <code>03-cloud-deployment/</code> thay vì <code>06-lab-complete/</code>.",
        "Không có Redis: <code>/ready</code> trả 503.",
        "Dùng Self-Test trong checklist: <code>GET /ask</code> ra 405, không phải 401.",
    )}
    {check("4 lệnh ra đúng 200 · 200 · 401 · 200 chưa? URL đã ghi vào <code>DEPLOYMENT.md</code> chưa?")}
  </div>
</div>
""",
    notes(
        "Việc của coach trong CP6",
        "Mục Lưu ý số 8 trong README có đủ bước Railway và Render.",
        "Render: <code>render.yaml</code> nằm trong thư mục con và phải tự khai báo Redis. Kẹt thì hỗ trợ tại bàn.",
        "Deploy chậm hoặc tài khoản bị kẹt: cho học viên sang CP7, quay lại deploy sau giờ lab.",
        "Che key khi chụp ảnh. Lệnh in mã HTTP không lộ key.",
    ),
    cp="6",
    minutes=25,
    label="CP6 · Deploy",
)

# 14 ── CP7 ──────────────────────────────────────────────────────────────
slide(
    "CP7: Benchmark local",
    f"""
<h2 class="title">CP7: đo tốc độ và độ đúng bằng số của bạn</h2>
{meta(when="17:15–18:00", where="<code>06-lab-complete/benchmark-observability/develop/</code>", write="<code>BENCHMARK_REPORT.md</code> ở gốc repo", out="JSON trong <code>develop/reports/</code>")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># 1. từ gốc repo, tạo báo cáo một lần</span>
cp -n 06-lab-complete/benchmark-observability/BENCHMARK_REPORT_TEMPLATE.md BENCHMARK_REPORT.md
cd 06-lab-complete/benchmark-observability/develop
AGENT_VERSION=v1 PORT=8001 python app.py   <span class="c"># terminal 1</span>
AGENT_VERSION=v2 PORT=8002 python app.py   <span class="c"># terminal 2</span>
<span class="c"># 2. load test 4 mức concurrency</span>
for c in 1 10 50 100; do
  python load_test.py --url http://localhost:8002 --requests 300 \\
    --concurrency "$c" --out "reports/load_v2_c${{c}}.json"
done
<span class="c"># 3–4. eval v1, v2; sửa KNOWLEDGE_BASE; bật lại v2</span>
python eval/run_eval.py --url http://localhost:8002 --min-accuracy 1.0 \\
  --baseline reports/eval_v2.json --out reports/eval_v2_fixed.json</pre>
  </div>
  <div class="stack">
    {coach(
        "So <code>MOCK_SLOW_RATE</code> = 0 · 0.03 · 0.1, mỗi lần <code>--requests 300 --concurrency 20</code>, lưu <code>load_v2_slow_*.json</code>.",
        "Eval v1 và v2 bằng hai lệnh ở Exercise 7.3, lưu <code>eval_v1.json</code>, <code>eval_v2.json</code>.",
        "Sửa <code>KNOWLEDGE_BASE</code> xong phải tắt và bật lại v2.",
    )}
    {anti(
        "Quên <code>--out</code>: không có file JSON để nộp.",
        "Eval không có <code>--url http://localhost:8002</code>: gọi nhầm cổng 8000.",
        "Sửa <code>golden_dataset.jsonl</code> thay vì <code>KNOWLEDGE_BASE</code>.",
    )}
    {check("Lệnh eval cuối in <code>Quality gate ... ✅ PASS</code> và có file <code>reports/eval_v2_fixed.json</code>?")}
  </div>
</div>
""",
    notes(
        "Câu hỏi gợi ý",
        "“Vì sao đặt SLO theo p95/p99, không theo trung bình?”",
        "“Vì sao ‘cost / câu đúng’ tốt hơn ‘cost / câu’ khi so hai phiên bản?”",
        "<code>load_test.py</code> trả exit code 1 khi vi phạm SLO nhưng vẫn lưu file. Không phải lỗi.",
        "Bước 5: job CI. Nộp file job, hoặc giải thích cách dùng exit code của <code>run_eval.py</code> để chặn merge.",
    ),
    cp="7",
    minutes=45,
    label="CP7 · Benchmark",
)

# 15 ── CP8 ──────────────────────────────────────────────────────────────
slide(
    "CP8: Observability stack (sau giờ lab)",
    f"""
<h2 class="title">CP8 (sau giờ lab): metrics, trace và alert</h2>
{meta(when="Sau 18:00, trước hạn nộp", where="<code>06-lab-complete/benchmark-observability/production/</code>", write="<code>BENCHMARK_REPORT.md</code>", out="2 file CSV Locust, 4 ảnh Part 7")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># bật stack bằng lệnh này, thay cho docker compose up của Exercise 7.4</span>
docker compose -p k5-day14-observability up -d --build --scale agent=1
docker compose -p k5-day14-observability run --rm locust \\
  -f /mnt/locust/locustfile.py --host http://nginx \\
  --headless -u 100 -r 10 -t 2m --csv /mnt/results/scale_1
docker compose -p k5-day14-observability up -d --scale agent=3
<span class="c"># chạy lại Locust với --csv /mnt/results/scale_3</span></pre>
    <section class="panel">
      <h3>4 ảnh Part 7 trong <code>screenshots/</code></h3>
      <p><code>grafana-dashboard.png</code> · <code>jaeger-slow-trace.png</code> · <code>jaeger-error-trace.png</code> · <code>prometheus-alert-firing.png</code> (trang Alerts, ≥ 2 alert cùng firing).</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "Locust phải chạy headless mới có file CSV.",
        "Trace chậm: ghi span chậm nhất và số ms. Chép dòng log JSON có cùng <code>trace_id</code>.",
        "Ghi thời gian từ lúc gây lỗi tới lúc alert firing.",
    )}
    {anti(
        "Dùng Locust giao diện web: không có CSV.",
        "Chạy <code>down -v</code> trước khi chụp ảnh và chép log.",
        "Số trong báo cáo không khớp CSV: mục đó 0 điểm.",
    )}
    {check("Có đủ <code>scale_1_stats.csv</code>, <code>scale_3_stats.csv</code> và 4 ảnh Part 7 chưa?")}
  </div>
</div>
""",
    notes(
        "Dặn trước khi tan lớp",
        "Stack có 6 dịch vụ (agent, nginx, prometheus, grafana, jaeger, locust). Máy cần RAM dư.",
        "Exercise 7.3 sửa <code>develop/utils/mock_llm.py</code>. Stack production dùng <code>production/utils/mock_llm.py</code>: muốn đạt 100% thì chép phần đã sửa sang.",
        "Dọn stack: <code>docker compose -p k5-day14-observability down -v</code>, sau khi đã chụp đủ ảnh.",
    ),
    cp="8",
    label="CP8 · Observability",
)

# 16 ── Rubric ───────────────────────────────────────────────────────────
RUBRIC_ROWS = [
    ("Part 1 · Localhost vs Production", "CP1", 8),
    ("Part 2 · Docker", "CP2", 8),
    ("Part 3 · Cloud Deployment", "CP6", 8),
    ("Part 4 · API Security", "CP3", 8),
    ("Part 5 · Scaling &amp; Reliability", "CP4", 8),
    ("Part 6 · Final Project", "CP5, CP6", 60),
    ("Part 7 · Load test &amp; SLO", "CP7", 4),
    ("Part 7 · Eval &amp; quality gate", "CP7", 5),
    ("Part 7 · Observability stack", "CP8", 4),
    ("Part 7 · Tracing", "CP8", 3),
    ("Part 7 · Alerts &amp; chaos", "CP8", 4),
]
assert sum(p for _, _, p in RUBRIC_ROWS) == 120
_rubric = "\n".join(
    f'      <tr><td>{name}</td><td>{cp}</td><td class="bar-cell" title="{pts} điểm"><span class="bar" style="--v: {pts / 60:.3f}"></span><span class="bar-val">{pts}</span></td></tr>'
    for name, cp, pts in RUBRIC_ROWS
)
slide(
    "Bảng điểm: tối đa 120, cần 70/100",
    f"""
<h2 class="title">Bảng điểm: tối đa 120 điểm, cần 70/100 để qua</h2>
<div class="grid grid-rubric">
  <table class="data data--compact">
    <thead><tr><th>Hạng mục</th><th>Checkpoint</th><th>Điểm</th></tr></thead>
    <tbody>
{_rubric}
    </tbody>
  </table>
  <div class="stack">
    <section class="panel">
      <h3>Part 6 (60 điểm): làm đúng thì đủ điểm, sai thì 0</h3>
      <p>Functional 15 · Docker &amp; cấu hình 10 · Security 15 · Reliability 10 · Deployment 10. Script chấm báo ❌ hoặc ⚠️ ở phần nào thì phần đó 0 điểm.</p>
    </section>
    <section class="anti">
      <h3>{{ICONS_ANTI}}Mất điểm khi</h3>
      <ul>
        <li>Commit <code>.env</code>, key hoặc token: −10.</li>
        <li>Số trong báo cáo không khớp JSON/CSV: mục Part 7 đó 0.</li>
        <li>Sai tên repo hoặc sai chỗ file: −5.</li>
        <li>Repo Private: không chấm.</li>
      </ul>
    </section>
    <p class="note">Điểm cuối = điểm bài × 100 / 120. Ví dụ: 84/120 thành 70/100. Lab này không có điểm thưởng.</p>
  </div>
</div>
""",
    notes(
        "Cách chấm (RUBRIC.md)",
        "Bước chấm đầu tiên: chạy <code>python check_production_ready.py</code> trong <code>06-lab-complete/</code> trên máy có Docker.",
        "Conversation history và các mục “Mở rộng” của Part 6 không tính điểm.",
        "URL deploy được chấm ở cả Part 3 và nhóm Deployment của Part 6.",
        "Nếu điểm chính thức đổi, sửa <code>RUBRIC_ROWS</code> trong <code>content/build_content.py</code>, rồi build lại.",
    ),
    done=8,
)

# 17 ── Submit checklist ─────────────────────────────────────────────────
slide(
    "Checklist nộp bài",
    """
<h2 class="title">Checklist nộp bài</h2>
<div class="grid grid-2">
  <div>
    <h3 class="sub">Trước khi nộp, kiểm:</h3>
    <ul class="checklist">
      <li>Tên repo đúng mẫu, repo Public, mở ở cửa sổ ẩn danh không bị 404.</li>
      <li><code>06-lab-complete/</code>: <code>python check_production_ready.py</code> báo <code>PASS 12/12</code> (bản đầy đủ).</li>
      <li><code>MISSION_ANSWERS.md</code>: Part 1–5, output script chấm, mục AI log.</li>
      <li><code>DEPLOYMENT.md</code>: URL chạy được, 4 lệnh CP6 ra 200 · 200 · 401 · 200.</li>
      <li><code>BENCHMARK_REPORT.md</code> điền đủ. <code>reports/</code>, <code>benchmark-results/</code>, 7 ảnh trong <code>screenshots/</code>.</li>
      <li>Số trong báo cáo khớp file JSON/CSV.</li>
      <li><code>git log --all --oneline -- '*.env' '.env'</code> không in gì.</li>
      <li>Nộp link repo trên LMS.</li>
    </ul>
  </div>
  <div class="stack">
    <section class="panel">
      <h3>Hạn nộp (GMT+7)</h3>
      <p class="deadline">{{DEADLINE}}</p>
      <p>Copy JSON và CSV ra gốc repo trước khi nộp (lệnh trong SUBMISSION.md). Không force-push, không sửa ngày commit.</p>
    </section>
    <div class="cta-row">
      <button class="btn-primary" type="button" onclick="window.kickoffLab && window.kickoffLab()">Bắt đầu CP0: Setup</button>
    </div>
  </div>
</div>
""",
    notes(
        "Lời dặn cuối",
        "Bấm nút để về CP0 và bắt đầu.",
        "Hạn nộp (GMT+7): 23h59 ngày lab, cho cả lớp sáng và lớp chiều. Lab Coach có thể thông báo hạn khác.",
        "Commit sau hạn không được chấm, trừ khi Lab Coach đồng ý trước (lý do sức khoẻ, sự cố kỹ thuật có bằng chứng).",
    ),
    done=8,
)

out = pathlib.Path(__file__).resolve().parent.parent / "app/src/slides/content.json"
out.write_text(json.dumps(S, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {len(S)} slides -> {out}")
