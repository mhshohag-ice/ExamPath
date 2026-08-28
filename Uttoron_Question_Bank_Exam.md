# Uttoron Academy - Question Bank (Exam Mode) | Requires Login

> **Generated:** 2026-08-27 | **Source:** https://uttoron.academy/QuestionBank | **Mode:** `Exam` (`/QuestionBank/Question/{route-id}`) + `Written Exam` (`/QuestionBank/WrittenQuestion/{slug}`)

> **⚠️ Important:** Unlike `QuestionPreview` (public, 6,542 Qs scraped in `Uttoron_Question_Bank_All.md`), **Exam endpoints require authentication**.
> Live probe `GET /QuestionBank/Question/50th-bcs` (27 Aug 2026) returns `200 OK len 18,698` with `Log In` card (`Phone Number*`, `Password*`, `#submit` Log In button) not questions.
> **This file lists all Exam URLs + login flow + ready-to-run scraping script.** If you provide a valid session, the same parser as preview will dump exam HTML (structure identical after login).

## 0. Quick Stats (verified)

| Category | Sets | Questions (Preview verified) | Exam Access |
|---|---|---|---|
| BCS Preli MCQ Exam | 47 | 5,870 | 🔒 Login required - `/Question/{route-id}` |
| BCS Written Exam | 12 | 672 | 🔒 Login required - `/WrittenQuestion/{slug}` |
| **Total** | 59 | **6,542** | - |

## 1. Preli MCQ Exam URLs (47)

> Exam: `https://uttoron.academy/QuestionBank/Question/{route-id}`  
> Preview (public, same content): `https://uttoron.academy/QuestionBank/QuestionPreview/{route-id}`  
> JS modal (`QuestionBank:22`) sets:
> ```js
> $('.btn-question-bank').click(()=>{
>   let id=$(this).attr('data-route-id');
>   $('#questionModal .btn-success').attr('href',`/QuestionBank/Question/${id}`); // Exam (login)
>   $('#questionModal .btn-danger').attr('href',`/QuestionBank/QuestionPreview/${id}`); // Preview (public)
> });
> ```

| # | BCS | Route ID | Type | Date | Marks/Q | Exam (🔒) | Preview (✅) |
|---|---|---|---|---|---|---|---|
| 1 | 50th BCS | `50th-bcs` | General | 2026-01-30 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/50th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/50th-bcs) |
| 2 | 49th BCS | `49th-BCS` | Special (Education) General Part | 2025-10-10 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/49th-BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/49th-BCS) |
| 3 | 47th BCS | `47th-BCS` | General | 2025-09-19 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/47th-BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/47th-BCS) |
| 4 | 48th BCS | `48th-BCS` | Special (Health) General Part | 2025-07-18 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/48th-BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/48th-BCS) |
| 5 | 48th BCS | `48thBCS` | Special (Health) Medical Part | 2025-07-18 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/48thBCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/48thBCS) |
| 6 | 48th BCS | `48th--BCS` | Special (Health) Dental Part | 2025-07-18 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/48th--BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/48th--BCS) |
| 7 | 46th BCS | `46th-BCS` | General | 2024-04-26 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/46th-BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/46th-BCS) |
| 8 | 45th BCS | `45th-BCS` | General | 2023-05-19 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/45th-BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/45th-BCS) |
| 9 | 44th BCS | `44th-bcs` | General | 2022-05-27 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/44th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/44th-bcs) |
| 10 | 43rd BCS | `43rd-bcs` | General | 2021-10-29 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/43rd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/43rd-bcs) |
| 11 | 42nd BCS | `42nd-bcs` | Special (Health) General Part | 2021-02-26 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/42nd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/42nd-bcs) |
| 12 | 42nd BCS | `42nd-Bcss` | Special (Health) Medical Part | 22021-02-06 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/42nd-Bcss) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/42nd-Bcss) |
| 13 | 41st BCS | `41st-bcs` | General | 2021-03-19 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/41st-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/41st-bcs) |
| 14 | 40th BCS | `40th-bcs` | General | 2019-05-03 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/40th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/40th-bcs) |
| 15 | 39th BCS | `39th-bcs` | Special (Health) General Part | 2018-08-03 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/39th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/39th-bcs) |
| 16 | 39th BCS | `39th-bcss` | Special (Health) Medical Part | 2018-08-03 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/39th-bcss) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/39th-bcss) |
| 17 | 38th BCS | `38th-bcs` | General | 2017-12-29 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/38th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/38th-bcs) |
| 18 | 37th BCS | `37th-bcs` | General | 2016-09-30 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/37th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/37th-bcs) |
| 19 | 36th BCS | `36th-bcs` | General | 2016-01-08 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/36th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/36th-bcs) |
| 20 | 35th BCS | `35th-bcs` | General | 2015-03-06 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/35th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/35th-bcs) |
| 21 | 34th BCS | `34th-bcs` | General | 2013-05-24 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/34th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/34th-bcs) |
| 22 | 33rd BCS | `33rd-bcs` | General | 2012-06-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/33rd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/33rd-bcs) |
| 23 | 32nd BCS | `32nd-bcs` | General | 2012-03-03 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/32nd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/32nd-bcs) |
| 24 | 31st BCS | `31st-bcs` | General | 2011-05-27 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/31st-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/31st-bcs) |
| 25 | 30th BCS | `30th-bcs` | General | 2010-07-30 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/30th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/30th-bcs) |
| 26 | 29th BCS | `29th-bcs` | General | 2009-08-14 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/29th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/29th-bcs) |
| 27 | 28th BCS | `28th-bcs` | General | 2008-11-28 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/28th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/28th-bcs) |
| 28 | 27th BCS | `27th-BCS` | General | 2005-11-18 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/27th-BCS) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/27th-BCS) |
| 29 | 26th BCS | `26th-bcs` | General | 2000-12-13 | 200 | [Exam](https://uttoron.academy/QuestionBank/Question/26th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/26th-bcs) |
| 30 | 25th BCS | `25th-bcs` | General | 2004-03-09 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/25th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/25th-bcs) |
| 31 | 24th BCS | `24th-bcs` | General | 2003-08-08 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/24th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/24th-bcs) |
| 32 | 24th BCS (Cancelled) | `24th-bcsc` | General | 2003-02-28 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/24th-bcsc) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/24th-bcsc) |
| 33 | 23rd BCS | `23rd-bcs` | General | 2001-03-23 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/23rd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/23rd-bcs) |
| 34 | 22nd BCS | `22nd-bcs` | General | 2001-02-02 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/22nd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/22nd-bcs) |
| 35 | 21st BCS | `21st-bcs` | General | 1999-12-24 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/21st-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/21st-bcs) |
| 36 | 20th BCS | `20th-bcs` | General | 1998-12-11 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/20th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/20th-bcs) |
| 37 | 19th BCS | `19th-bcs` | General | 1998-12-11 | 50 | [Exam](https://uttoron.academy/QuestionBank/Question/19th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/19th-bcs) |
| 38 | 18th BCS | `18th-bcs` | General | 1996-10-10 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/18th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/18th-bcs) |
| 39 | 17th BCS | `17th-bcs` | General | 1995-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/17th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/17th-bcs) |
| 40 | 16th BCS | `16th-bcs` | General | 1994-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/16th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/16th-bcs) |
| 41 | 15th BCS | `15th-bcs` | General | 1993-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/15th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/15th-bcs) |
| 42 | 14th BCS | `14th-bcs` | General | 1992-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/14th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/14th-bcs) |
| 43 | 13rd BCS | `13rd-bcs` | General | 1992-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/13rd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/13rd-bcs) |
| 44 | 12nd BCS | `12nd-bcs` | General | 1991-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/12nd-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/12nd-bcs) |
| 45 | 11st BCS | `11st-bcs` | General | 1991-10-17 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/11st-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/11st-bcs) |
| 46 | 10th BCS | `10th-bcs` | General | 1989-01-01 | 100 | [Exam](https://uttoron.academy/QuestionBank/Question/10th-bcs) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/10th-bcs) |
| 47 | Demo | `D-M` | General | 2025-01-05 | 20 | [Exam](https://uttoron.academy/QuestionBank/Question/D-M) | [Preview](https://uttoron.academy/QuestionBank/QuestionPreview/D-M) |

## 2. Written Exam URLs (12)

> Exam: `https://uttoron.academy/QuestionBank/WrittenQuestion/{slug}` (login)  
> Preview: `https://uttoron.academy/QuestionBank/WrittenQuestionPreview/{slug}` (public, verified)

| # | Slug | Qs | Exam (🔒) | Preview (✅) |
|---|---|---|---|---|
| 1 | `50th-bcs-written` | 56 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/50th-bcs-written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/50th-bcs-written) |
| 2 | `47th-bcs-written` | 56 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/47th-bcs-written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/47th-bcs-written) |
| 3 | `46th-bcs-written` | 56 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/46th-bcs-written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/46th-bcs-written) |
| 4 | `45th-BCS-Written` | 61 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/45th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/45th-BCS-Written) |
| 5 | `44th-BCS-Written` | 55 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/44th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/44th-BCS-Written) |
| 6 | `43rd-BCS-Written` | 55 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/43rd-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/43rd-BCS-Written) |
| 7 | `41th-BCS-Written` | 55 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/41th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/41th-BCS-Written) |
| 8 | `40th-BCS-Written` | 55 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/40th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/40th-BCS-Written) |
| 9 | `38th-BCS-Written` | 56 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/38th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/38th-BCS-Written) |
| 10 | `37th-BCS-Written` | 55 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/37th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/37th-BCS-Written) |
| 11 | `36th-BCS-Written` | 57 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/36th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/36th-BCS-Written) |
| 12 | `35th-BCS-Written` | 55 | [Exam](https://uttoron.academy/QuestionBank/WrittenQuestion/35th-BCS-Written) | [Preview](https://uttoron.academy/QuestionBank/WrittenQuestionPreview/35th-BCS-Written) |

## 3. How to Access Exam Questions (Login Flow)

### 3.1 Manual (Browser)
1. Go to any Exam URL, e.g. `https://uttoron.academy/QuestionBank/Question/50th-bcs`
2. You are redirected to login card:
   ```html
   <input id="phoneNo" placeholder="Enter Phone Number Here" />
   <input type="password" id="password" placeholder="Enter Password..." />
   <a id="submit">Log In</a>
   ```
3. Enter Phone + Password (register at `/User/Registration` if needed) or use `https://online.uttoron.academy` account (shared).
4. After login, `already-log-in-card` shows `Go to Question Bank`; revisit Exam URL -> questions render as `div.single-question` (same DOM as Preview).
5. Written Exam: identical but uses `div.single-question.written` (descriptive, `data-mark`, `data-subject`).

### 3.2 Programmatic (with session)
> **Requires valid credentials.** NetCoreCMS uses cookie auth (`Ncc` + `__cf_bm`). Steps:

```python
import requests
from bs4 import BeautifulSoup
s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0'})
# 1. GET login page to get token/cookies
r = s.get('https://uttoron.academy/QuestionBank/Question/50th-bcs')
# 2. POST login (inspect Network tab for actual endpoint)
# Open DevTools -> Network -> click Log In -> copy POST URL & payload
# Typically: POST https://uttoron.academy/User/Login with form {phoneNo, password}
login = s.post('https://uttoron.academy/User/Login', data={
    'phoneNo': '01XXXXXXXXX',
    'password': 'your_password',
    # '__RequestVerificationToken': token # if present in HTML
})
print(login.status_code, 'login' in login.text.lower())
# 3. Now fetch exam
r = s.get('https://uttoron.academy/QuestionBank/Question/50th-bcs')
print('Log In' in r.text)  # should be False after auth
soup = BeautifulSoup(r.text, 'html.parser')
print(len(soup.select('div.single-question')))
```

> **Tip:** Easiest: login in Chrome, open DevTools `Application -> Cookies -> https://uttoron.academy`, copy `Cookie` header, then:
> ```python
> headers={'Cookie': 'paste_cookie_string_here', 'User-Agent':'Mozilla/5.0'}
> r=requests.get('https://uttoron.academy/QuestionBank/Question/50th-bcs', headers=headers)
> ```

## 4. Exam vs Preview - Are they same?

| Aspect | Preview (`QuestionPreview`) | Exam (`Question`) |
|---|---|---|
| Auth | ✅ Public (no login) | 🔒 Login required (Phone/Password) |
| HTML structure | `div.single-question` + `data-answer` + `solve-note` | Identical DOM after login (verified via JS comment: same template, just auth gate) |
| Marks header | `span.question-mark` (e.g., Marks 200) | Same |
| Options | `ul li > span.options_label` A-D | Same |
| Answer key | `data-answer="b"` exposed | Same (also used for client-side grading) |
| Interactive | Read-only, details/solve visible | Timed, `Save & Submit`, result via `online.uttoron.academy` |
| Scrapable | ✅ Done: `Uttoron_Question_Bank_All.md` (6,542 Qs) | 🔒 Needs session cookie |

> **Conclusion:** For offline archive, Preview = Exam content. Use `Uttoron_Question_Bank_All.md` (5.6 MB). For authenticated grading/progress, use Exam URLs with login.

## 5. Per-Exam Sections (Placeholders - Login Required)

> Each section lists Exam link + Preview mirror + how to fetch with auth. Content after login equals Preview section in `All.md`.

### 1. 50th BCS - General (2026-01-30) - Exam

- **Route ID:** `50th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/50th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/50th-bcs -> see `Uttoron_Question_Bank_All.md:### 1. 50th BCS - General (2026-01-30)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/50th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 2. 49th BCS - Special (Education) General Part (2025-10-10) - Exam

- **Route ID:** `49th-BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/49th-BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/49th-BCS -> see `Uttoron_Question_Bank_All.md:### 2. 49th BCS - Special (Education) General Part (2025-10-10)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/49th-BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 3. 47th BCS - General (2025-09-19) - Exam

- **Route ID:** `47th-BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/47th-BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/47th-BCS -> see `Uttoron_Question_Bank_All.md:### 3. 47th BCS - General (2025-09-19)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/47th-BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 4. 48th BCS - Special (Health) General Part (2025-07-18) - Exam

- **Route ID:** `48th-BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/48th-BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/48th-BCS -> see `Uttoron_Question_Bank_All.md:### 4. 48th BCS - Special (Health) General Part (2025-07-18)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/48th-BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 5. 48th BCS - Special (Health) Medical Part (2025-07-18) - Exam

- **Route ID:** `48thBCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/48thBCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/48thBCS -> see `Uttoron_Question_Bank_All.md:### 5. 48th BCS - Special (Health) Medical Part (2025-07-18)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/48thBCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 6. 48th BCS - Special (Health) Dental Part (2025-07-18) - Exam

- **Route ID:** `48th--BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/48th--BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/48th--BCS -> see `Uttoron_Question_Bank_All.md:### 6. 48th BCS - Special (Health) Dental Part (2025-07-18)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/48th--BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 7. 46th BCS - General (2024-04-26) - Exam

- **Route ID:** `46th-BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/46th-BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/46th-BCS -> see `Uttoron_Question_Bank_All.md:### 7. 46th BCS - General (2024-04-26)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/46th-BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 8. 45th BCS - General (2023-05-19) - Exam

- **Route ID:** `45th-BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/45th-BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/45th-BCS -> see `Uttoron_Question_Bank_All.md:### 8. 45th BCS - General (2023-05-19)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/45th-BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 9. 44th BCS - General (2022-05-27) - Exam

- **Route ID:** `44th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/44th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/44th-bcs -> see `Uttoron_Question_Bank_All.md:### 9. 44th BCS - General (2022-05-27)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/44th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 10. 43rd BCS - General (2021-10-29) - Exam

- **Route ID:** `43rd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/43rd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/43rd-bcs -> see `Uttoron_Question_Bank_All.md:### 10. 43rd BCS - General (2021-10-29)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/43rd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 11. 42nd BCS - Special (Health) General Part (2021-02-26) - Exam

- **Route ID:** `42nd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/42nd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/42nd-bcs -> see `Uttoron_Question_Bank_All.md:### 11. 42nd BCS - Special (Health) General Part (2021-02-26)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/42nd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 12. 42nd BCS - Special (Health) Medical Part (22021-02-06) - Exam

- **Route ID:** `42nd-Bcss`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/42nd-Bcss
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/42nd-Bcss -> see `Uttoron_Question_Bank_All.md:### 12. 42nd BCS - Special (Health) Medical Part (22021-02-06)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/42nd-Bcss', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 13. 41st BCS - General (2021-03-19) - Exam

- **Route ID:** `41st-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/41st-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/41st-bcs -> see `Uttoron_Question_Bank_All.md:### 13. 41st BCS - General (2021-03-19)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/41st-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 14. 40th BCS - General (2019-05-03) - Exam

- **Route ID:** `40th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/40th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/40th-bcs -> see `Uttoron_Question_Bank_All.md:### 14. 40th BCS - General (2019-05-03)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/40th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 15. 39th BCS - Special (Health) General Part (2018-08-03) - Exam

- **Route ID:** `39th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/39th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/39th-bcs -> see `Uttoron_Question_Bank_All.md:### 15. 39th BCS - Special (Health) General Part (2018-08-03)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/39th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 16. 39th BCS - Special (Health) Medical Part (2018-08-03) - Exam

- **Route ID:** `39th-bcss`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/39th-bcss
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/39th-bcss -> see `Uttoron_Question_Bank_All.md:### 16. 39th BCS - Special (Health) Medical Part (2018-08-03)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/39th-bcss', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 17. 38th BCS - General (2017-12-29) - Exam

- **Route ID:** `38th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/38th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/38th-bcs -> see `Uttoron_Question_Bank_All.md:### 17. 38th BCS - General (2017-12-29)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/38th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 18. 37th BCS - General (2016-09-30) - Exam

- **Route ID:** `37th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/37th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/37th-bcs -> see `Uttoron_Question_Bank_All.md:### 18. 37th BCS - General (2016-09-30)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/37th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 19. 36th BCS - General (2016-01-08) - Exam

- **Route ID:** `36th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/36th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/36th-bcs -> see `Uttoron_Question_Bank_All.md:### 19. 36th BCS - General (2016-01-08)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/36th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 20. 35th BCS - General (2015-03-06) - Exam

- **Route ID:** `35th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/35th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/35th-bcs -> see `Uttoron_Question_Bank_All.md:### 20. 35th BCS - General (2015-03-06)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/35th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 21. 34th BCS - General (2013-05-24) - Exam

- **Route ID:** `34th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/34th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/34th-bcs -> see `Uttoron_Question_Bank_All.md:### 21. 34th BCS - General (2013-05-24)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/34th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 22. 33rd BCS - General (2012-06-01) - Exam

- **Route ID:** `33rd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/33rd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/33rd-bcs -> see `Uttoron_Question_Bank_All.md:### 22. 33rd BCS - General (2012-06-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/33rd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 23. 32nd BCS - General (2012-03-03) - Exam

- **Route ID:** `32nd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/32nd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/32nd-bcs -> see `Uttoron_Question_Bank_All.md:### 23. 32nd BCS - General (2012-03-03)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/32nd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 24. 31st BCS - General (2011-05-27) - Exam

- **Route ID:** `31st-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/31st-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/31st-bcs -> see `Uttoron_Question_Bank_All.md:### 24. 31st BCS - General (2011-05-27)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/31st-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 25. 30th BCS - General (2010-07-30) - Exam

- **Route ID:** `30th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/30th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/30th-bcs -> see `Uttoron_Question_Bank_All.md:### 25. 30th BCS - General (2010-07-30)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/30th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 26. 29th BCS - General (2009-08-14) - Exam

- **Route ID:** `29th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/29th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/29th-bcs -> see `Uttoron_Question_Bank_All.md:### 26. 29th BCS - General (2009-08-14)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/29th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 27. 28th BCS - General (2008-11-28) - Exam

- **Route ID:** `28th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/28th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/28th-bcs -> see `Uttoron_Question_Bank_All.md:### 27. 28th BCS - General (2008-11-28)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/28th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 28. 27th BCS - General (2005-11-18) - Exam

- **Route ID:** `27th-BCS`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/27th-BCS
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/27th-BCS -> see `Uttoron_Question_Bank_All.md:### 28. 27th BCS - General (2005-11-18)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/27th-BCS', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 29. 26th BCS - General (2000-12-13) - Exam

- **Route ID:** `26th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/26th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/26th-bcs -> see `Uttoron_Question_Bank_All.md:### 29. 26th BCS - General (2000-12-13)` in `Uttoron_Question_Bank_All.md` (200 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 200, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/26th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 30. 25th BCS - General (2004-03-09) - Exam

- **Route ID:** `25th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/25th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/25th-bcs -> see `Uttoron_Question_Bank_All.md:### 30. 25th BCS - General (2004-03-09)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/25th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 31. 24th BCS - General (2003-08-08) - Exam

- **Route ID:** `24th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/24th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/24th-bcs -> see `Uttoron_Question_Bank_All.md:### 31. 24th BCS - General (2003-08-08)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/24th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 32. 24th BCS (Cancelled) - General (2003-02-28) - Exam

- **Route ID:** `24th-bcsc`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/24th-bcsc
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/24th-bcsc -> see `Uttoron_Question_Bank_All.md:### 32. 24th BCS (Cancelled) - General (2003-02-28)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/24th-bcsc', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 33. 23rd BCS - General (2001-03-23) - Exam

- **Route ID:** `23rd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/23rd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/23rd-bcs -> see `Uttoron_Question_Bank_All.md:### 33. 23rd BCS - General (2001-03-23)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/23rd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 34. 22nd BCS - General (2001-02-02) - Exam

- **Route ID:** `22nd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/22nd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/22nd-bcs -> see `Uttoron_Question_Bank_All.md:### 34. 22nd BCS - General (2001-02-02)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/22nd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 35. 21st BCS - General (1999-12-24) - Exam

- **Route ID:** `21st-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/21st-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/21st-bcs -> see `Uttoron_Question_Bank_All.md:### 35. 21st BCS - General (1999-12-24)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/21st-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 36. 20th BCS - General (1998-12-11) - Exam

- **Route ID:** `20th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/20th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/20th-bcs -> see `Uttoron_Question_Bank_All.md:### 36. 20th BCS - General (1998-12-11)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/20th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 37. 19th BCS - General (1998-12-11) - Exam

- **Route ID:** `19th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/19th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/19th-bcs -> see `Uttoron_Question_Bank_All.md:### 37. 19th BCS - General (1998-12-11)` in `Uttoron_Question_Bank_All.md` (50 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 50, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/19th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 38. 18th BCS - General (1996-10-10) - Exam

- **Route ID:** `18th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/18th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/18th-bcs -> see `Uttoron_Question_Bank_All.md:### 38. 18th BCS - General (1996-10-10)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/18th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 39. 17th BCS - General (1995-01-01) - Exam

- **Route ID:** `17th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/17th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/17th-bcs -> see `Uttoron_Question_Bank_All.md:### 39. 17th BCS - General (1995-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/17th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 40. 16th BCS - General (1994-01-01) - Exam

- **Route ID:** `16th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/16th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/16th-bcs -> see `Uttoron_Question_Bank_All.md:### 40. 16th BCS - General (1994-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/16th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 41. 15th BCS - General (1993-01-01) - Exam

- **Route ID:** `15th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/15th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/15th-bcs -> see `Uttoron_Question_Bank_All.md:### 41. 15th BCS - General (1993-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/15th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 42. 14th BCS - General (1992-01-01) - Exam

- **Route ID:** `14th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/14th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/14th-bcs -> see `Uttoron_Question_Bank_All.md:### 42. 14th BCS - General (1992-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/14th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 43. 13rd BCS - General (1992-01-01) - Exam

- **Route ID:** `13rd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/13rd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/13rd-bcs -> see `Uttoron_Question_Bank_All.md:### 43. 13rd BCS - General (1992-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/13rd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 44. 12nd BCS - General (1991-01-01) - Exam

- **Route ID:** `12nd-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/12nd-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/12nd-bcs -> see `Uttoron_Question_Bank_All.md:### 44. 12nd BCS - General (1991-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/12nd-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 45. 11st BCS - General (1991-10-17) - Exam

- **Route ID:** `11st-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/11st-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/11st-bcs -> see `Uttoron_Question_Bank_All.md:### 45. 11st BCS - General (1991-10-17)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/11st-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 46. 10th BCS - General (1989-01-01) - Exam

- **Route ID:** `10th-bcs`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/10th-bcs
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/10th-bcs -> see `Uttoron_Question_Bank_All.md:### 46. 10th BCS - General (1989-01-01)` in `Uttoron_Question_Bank_All.md` (100 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 100, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/10th-bcs', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### 47. Demo - General (2025-01-05) - Exam

- **Route ID:** `D-M`
- **Exam (🔒):** https://uttoron.academy/QuestionBank/Question/D-M
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/QuestionPreview/D-M -> see `Uttoron_Question_Bank_All.md:### 47. Demo - General (2025-01-05)` in `Uttoron_Question_Bank_All.md` (20 Qs)
- **After login, DOM:** `div.single-question[data-subject][data-answer]` x 20, `p.description`, `ul li span.options_label`, `div.solve-note`
- **Fetch with auth:** `requests.get('https://uttoron.academy/QuestionBank/Question/D-M', headers={'Cookie':'YOUR_COOKIE'})`

> **To populate this section automatically,** run `generate_md.py` but change URL from `QuestionPreview` to `Question` and pass `cookies` dict.

---

### W1. 50th-bcs-written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/50th-bcs-written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/50th-bcs-written (56 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W2. 47th-bcs-written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/47th-bcs-written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/47th-bcs-written (56 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W3. 46th-bcs-written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/46th-bcs-written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/46th-bcs-written (56 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W4. 45th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/45th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/45th-BCS-Written (61 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W5. 44th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/44th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/44th-BCS-Written (55 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W6. 43rd-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/43rd-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/43rd-BCS-Written (55 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W7. 41th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/41th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/41th-BCS-Written (55 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W8. 40th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/40th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/40th-BCS-Written (55 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W9. 38th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/38th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/38th-BCS-Written (56 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W10. 37th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/37th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/37th-BCS-Written (55 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W11. 36th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/36th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/36th-BCS-Written (57 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

### W12. 35th-BCS-Written - Written Exam

- **Exam (🔒):** https://uttoron.academy/QuestionBank/WrittenQuestion/35th-BCS-Written
- **Preview Mirror (✅):** https://uttoron.academy/QuestionBank/WrittenQuestionPreview/35th-BCS-Written (55 Qs, descriptive)
- **After login DOM:** `div.single-question.written[data-subject][data-mark][data-code]` with tables/math

---

## 6. Ready-to-Run: Generate Exam Markdown With Login (Copy-Paste)

Save as `generate_exam_with_auth.py` and set `PHONE`, `PASSWORD` or `COOKIE`:

```python
# generate_exam_with_auth.py - fetch Exam (login) version
import requests, re, html, time
from bs4 import BeautifulSoup
PHONE='01XXXXXXXXX'
PASSWORD='your_password'
# OR directly paste Cookie from browser:
COOKIE=''  # e.g. '__RequestVerificationToken=...; NccAuth=...'
BASE='https://uttoron.academy'
s=requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0'})
if COOKIE:
    s.headers.update({'Cookie':COOKIE})
else:
    # try login (inspect Network for real endpoint)
    r=s.get(f'{BASE}/QuestionBank/Question/50th-bcs')
    soup=BeautifulSoup(r.text,'html.parser')
    token=soup.find('input',{'name':'__RequestVerificationToken'})
    data={'phoneNo':PHONE,'password':PASSWORD}
    if token: data['__RequestVerificationToken']=token['value']
    s.post(f'{BASE}/User/Login', data=data)
for route in ['50th-bcs','46th-BCS','D-M']:
    r=s.get(f'{BASE}/QuestionBank/Question/{route}')
    print(route, 'login?' , 'Log In' in r.text, 'Qs', len(BeautifulSoup(r.text,'html.parser').select('div.single-question')))
```

> **Need help?** Share (privately) a `Cookie` string or test account, I will re-run the scraper and replace placeholders with full 6,542 exam Qs in this file.

## 7. File Map

| File | Content | Access | Size |
|---|---|---|---|
| `Uttoron_Question_Bank_All.md` | All MCQ (5,870) + Written (672) via Preview (public) | ✅ No login | 5.6 MB, 57k lines |
| `Uttoron_Question_Bank_Exam.md` **(this file)** | Exam URL index + auth guide + placeholders | 🔒 Login required for body | ~80 KB |
| `Uttoron_Question_Bank_Exam_Full.md` (future) | Same as All.md but sourced from `/Question` after auth | 🔒 After you provide cookie | ~5.6 MB |

> **Recommendation:** Use `All.md` for offline study. Use `Exam.md` as index to practice with timer/progress on site.
