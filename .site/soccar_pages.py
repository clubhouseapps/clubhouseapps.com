#!/usr/bin/env python3
"""Build the SoccAR text pages from DinnerPilot's privacy page template (shared head/header/footer markers kept)."""
import re, sys, pathlib

SITE = pathlib.Path(sys.argv[1])
tpl = (SITE / "dinnerpilot/privacy/index.html").read_text()

SIDE_ITEMS = [
    ("/soccar/", "About SoccAR"),
    ("/soccar/privacy/", "Privacy policy"),
    ("/soccar/terms/", "Terms of service"),
    ("/soccar/data-deletion/", "Delete your data"),
    ("/soccar/account/", "Account help"),
]
MAIL = '<a href="mailto:support@clubhouseapps.com">support@clubhouseapps.com</a>'

def side(cur):
    current = ' aria-current="page"'
    lis = "".join(
        f'<li><a href="{h}"{current if h == cur else ""}>{t}</a></li>' for h, t in SIDE_ITEMS
    )
    return f'''<aside class="doc__side span-3" aria-label="SoccAR help">
        <p class="t-label">SoccAR help</p>
        <ul>{lis}</ul>
        <a class="link" href="/#apps">More from Clubhouse Apps</a>
      </aside>'''

def page(rel, title, desc, h1, updated, prose):
    s = tpl
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://clubhouseapps.com/{rel}">', s)
    s = re.sub(r'<aside class="doc__side.*?</aside>', side("/" + rel), s, flags=re.S)
    upd = ('<p class="doc__updated">Last updated: %s</p>' % updated) if updated else ""
    head = f'''<header class="doc__head">
          <a class="t-label" href="/soccar/">SoccAR</a>
          <h1>{h1}</h1>
          {upd}
        </header>'''
    s = re.sub(r'<header class="doc__head">.*?</header>', head, s, flags=re.S)
    s = re.sub(r'<div class="prose">.*?</div>\n      </article>', f'<div class="prose">\n{prose}\n        </div>\n      </article>', s, flags=re.S)
    assert "inner" not in s or True
    out = SITE / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    # Header/footer still point at DinnerPilot until stamp.py runs; everything else must be SoccAR.
    body = s.split("<!-- /site:header -->")[1].split("<!-- site:footer-links -->")[0]
    assert "dinnerpilot" not in body.lower(), rel
    print("wrote", rel)

UPDATED = "November 26, 2026"

landing = f'''  <p class="t-lead">SoccAR lets a soccer coach lay out a drill&rsquo;s cones on the real field through an iPhone camera, before a single cone comes out of the bag.</p>
  <p>Pick a drill from the library, aim at the grass, and tap once. The whole layout appears where you aimed, life-size, with the distance between cones marked in yards. Turn it, slide it, then walk the field and put a real cone on each virtual one.</p>

  <h2>What it does</h2>
  <ul>
    <li><strong>A drill library.</strong> More than 30 layouts across warm-ups, dribbling, passing, possession, shooting, defending, agility and small-sided games, with standard field and goal sizes for 3v3 up to 9v9.</li>
    <li><strong>One tap to place.</strong> The aiming ring turns green when the ground is found. One tap places the drill; tap Clear to start again.</li>
    <li><strong>Find your cones.</strong> A tall center pin marks the middle of the drill, and an arrow at the edge of the screen points the way when it is out of view.</li>
    <li><strong>Turn and move.</strong> Rotate the layout in 15&deg; or 90&deg; steps, or drag it into place.</li>
    <li><strong>Teams and history.</strong> Keep a separate list for each team you coach and see which drills each team ran on which day.</li>
    <li><strong>Tabletop mode.</strong> Shrink any drill onto a table to walk your players through it.</li>
  </ul>

  <h2>Coaching with others</h2>
  <p>Coach accounts let you sign in with email, Apple or Google and invite assistant coaches to a team with a code, so everyone sees the same team and the same drill history.</p>

  <h2>How to get it</h2>
  <p>SoccAR is in a private beta on TestFlight for iPhone. It needs an iPhone that supports ARKit (an iPhone XS or later). To ask about the beta, email {MAIL}.</p>

  <h2>Help</h2>
  <ul>
    <li><a href="/soccar/account/">Account help</a>: password resets and email links</li>
    <li><a href="/soccar/data-deletion/">Delete your data</a></li>
    <li><a href="/soccar/privacy/">Privacy policy</a> and <a href="/soccar/terms/">Terms of service</a></li>
  </ul>'''

privacy = f'''  <p>Clubhouse Apps ("we," "our," or "us") operates the SoccAR iOS application and the ClubhouseApps.com website. This Privacy Policy explains what information SoccAR collects, how we use it, and your rights regarding your data.</p>
  <p>By using SoccAR, you agree to the practices described in this policy. If you do not agree, please do not use the app.</p>

  <h2>1. Information We Collect</h2>
  <p><strong>Account information:</strong> When you create a coach account, we collect your email address and, if you sign in with Apple or Google, your name (if you choose to share it). If you sign up with an email address and password, your password is stored by our authentication provider in hashed form; we never see it.</p>
  <p><strong>Teams and coaches:</strong> We store the names of the teams you create, which coaches belong to each team and their role (owner or coach), and the invite codes you create to add other coaches, including when each code expires and which account used it.</p>
  <p><strong>Drill history:</strong> When you place a drill for a team, we record which drill it was, its category, the day, and which coach logged it. The other coaches on that team can see this history.</p>
  <p><strong>Camera:</strong> SoccAR uses your iPhone&rsquo;s camera and motion sensors to find the ground and show cones on it. This is processed on your iPhone by Apple&rsquo;s ARKit. We do not record, store or upload camera images or video, and the app does not take photos.</p>
  <p><strong>Information kept on your iPhone:</strong> Your teams and drill history are also stored on your iPhone so the app works on the field without a signal. Your chosen drill, cone color and other settings stay on your iPhone.</p>
  <p><strong>Device and usage information:</strong> SoccAR contains no advertising, no third-party analytics, and no crash-reporting tools. We do not collect location data. If you install SoccAR through TestFlight, Apple may share crash reports and feedback you choose to send with us, under Apple&rsquo;s terms.</p>

  <h2>2. How We Use Your Information</h2>
  <ul>
    <li>To create and secure your account and sign you in</li>
    <li>To keep your teams and drill history in sync across your devices and with the coaches you invite</li>
    <li>To send service emails, such as confirming your email address and resetting your password (never marketing without your consent)</li>
    <li>To respond to you when you contact us for support</li>
  </ul>

  <h2>3. Third-Party Services</h2>
  <p>We share data with the following third parties to operate SoccAR:</p>
  <ul>
    <li><strong>Supabase</strong> — Cloud database and authentication provider. Stores your account, teams and drill history. Hosted in the United States.</li>
    <li><strong>Resend</strong> — Sends account emails (email confirmation and password reset) to your address.</li>
    <li><strong>Apple Sign-In</strong> — Optional sign-in method. Governed by Apple&rsquo;s Privacy Policy.</li>
    <li><strong>Google Sign-In</strong> — Optional sign-in method. Governed by Google&rsquo;s Privacy Policy.</li>
    <li><strong>Apple TestFlight</strong> — Distributes the beta app. Governed by Apple&rsquo;s terms and privacy policy.</li>
    <li><strong>Cloudflare and GitHub Pages</strong> — Serve this website.</li>
  </ul>
  <p>We do not sell your personal data to any third party, and we do not use it for advertising.</p>

  <h2>4. Who Can See Your Information</h2>
  <p>Coaches on a team you belong to can see the team&rsquo;s name, the drill history for that team, and the names of the other coaches on it. Nobody else can see your teams. Anyone with a valid invite code you created can join that team until the code is used or expires, so share codes only with coaches you trust.</p>

  <h2>5. Data Retention</h2>
  <p>We keep your data for as long as your account is active. You can delete your account at any time (see Section 9). Unused invite codes expire after 7 days.</p>

  <h2>6. Children&rsquo;s Privacy (COPPA)</h2>
  <p>SoccAR is made for adult coaches and is not directed at children under 13. We do not collect information about the players on your teams, and you should not enter players&rsquo; personal information as team names. We do not knowingly collect personal information from children under 13. If you believe we have, please contact us and we will delete it.</p>

  <h2>7. Your Rights — GDPR (European Users)</h2>
  <p>If you are located in the European Economic Area, you have the right to access, correct, delete, and receive a portable copy of your personal data, and to object to certain processing. To exercise any of these rights, email us at {MAIL}. We will respond within 30 days.</p>

  <h2>8. Your Rights — CCPA (California Users)</h2>
  <p>If you are a California resident, you have the right to know what personal information we collect, the right to request deletion, and the right to opt out of the sale of your personal information. <strong>We do not sell your personal information.</strong> To exercise your rights, contact us at {MAIL}.</p>

  <h2>9. Account and Data Deletion</h2>
  <p>You can delete your SoccAR account from within the app, or by emailing {MAIL}. Deleting your account permanently removes your profile, the teams you created (with their drill history and invite codes) and your place on other coaches&rsquo; teams. Drill entries you logged on another coach&rsquo;s team stay with that team but are no longer linked to you. For details, see our <a href="/soccar/data-deletion/">Data Deletion page</a>.</p>

  <h2>10. Cookies and Tracking (Website)</h2>
  <p>The SoccAR pages on ClubhouseApps.com use no advertising cookies or third-party tracking scripts. Cloudflare may set cookies for security and performance purposes. The email confirmation and account pages contact Supabase only when you tap a button on them.</p>

  <h2>11. Security</h2>
  <p>We use encrypted connections (TLS), row-level security on our database so each coach can reach only their own teams, and token-based authentication. No method of transmission over the internet is 100% secure, but we take reasonable precautions to protect your data.</p>

  <h2>12. Changes to This Policy</h2>
  <p>We may update this Privacy Policy from time to time. When we do, we will update the "Last updated" date at the top of this page, and for material changes we will notify you within the app. Your continued use of SoccAR after changes are posted means you accept the revised policy.</p>

  <h2>13. Contact Us</h2>
  <p><strong>Clubhouse Apps</strong><br />
  Email: {MAIL}<br />
  Website: <a href="https://clubhouseapps.com">clubhouseapps.com</a></p>'''

terms = f'''  <p>These Terms of Service ("Terms") govern your use of SoccAR, provided by Clubhouse Apps ("we," "our," or "us"). By downloading or using SoccAR, you agree to these Terms. If you do not agree, do not use the app.</p>

  <h2>1. Description of Service</h2>
  <p>SoccAR is an iOS application that uses augmented reality to show soccer drill layouts on a real field, so a coach can see where to place cones. It includes a library of drill layouts, team lists, drill history, and shared teams for coaches who work together. SoccAR is currently offered free of charge as a beta through Apple&rsquo;s TestFlight.</p>

  <h2>2. Beta Software</h2>
  <p>SoccAR is pre-release software. Features may change, stop working, or be removed, and data may be lost. Please keep your own record of anything you cannot afford to lose. Beta builds expire on the schedule Apple sets for TestFlight.</p>

  <h2>3. Eligibility</h2>
  <p>You must be at least 18 years old, or the age of majority where you live, to create a SoccAR account.</p>

  <h2>4. Accounts and Shared Teams</h2>
  <p>You are responsible for keeping your sign-in details private and for all activity under your account. Notify us at {MAIL} if you suspect unauthorized access.</p>
  <p>When you invite another coach to a team, that coach can see and add to the team&rsquo;s drill history. The coach who created a team can remove other coaches from it. Share invite codes only with people you want on your team.</p>
  <p>We may suspend or terminate accounts that violate these Terms.</p>

  <h2>5. Safety on the Field</h2>
  <p><strong>Watch where you are going.</strong> Do not walk or run while looking at your screen near players, balls, goals, traffic, water or other hazards. Stay aware of your surroundings at all times.</p>
  <p><strong>Placement is approximate.</strong> Augmented reality tracking can drift, especially over long distances, on plain or uneven ground, or in poor light. Cone positions and distances shown in the app are estimates. Check measurements yourself when they matter.</p>
  <p><strong>Drills are for guidance only.</strong> The drill layouts are general examples. You are responsible for choosing activities that are safe and suitable for your players&rsquo; ages, abilities and conditions, and for following the rules of your club, league and governing body.</p>

  <h2>6. Acceptable Use</h2>
  <p>You agree not to:</p>
  <ul>
    <li>Use SoccAR for any unlawful purpose</li>
    <li>Attempt to reverse engineer, decompile, or extract the source code of the app</li>
    <li>Use automated tools to access the app or its servers</li>
    <li>Access, or try to access, teams or accounts that are not yours</li>
    <li>Enter players&rsquo; personal information, or anything illegal, harmful or offensive, as team names</li>
  </ul>

  <h2>7. Intellectual Property</h2>
  <p>SoccAR, its design, code, branding, and drill library are the property of Clubhouse Apps and protected by applicable intellectual property laws. You are granted a limited, non-exclusive, non-transferable license to use the app for coaching. Team names and drill history you create remain yours; you grant us a limited license to store and process them to provide the service.</p>

  <h2>8. Disclaimers</h2>
  <p>SOCCAR IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SERVICE WILL BE UNINTERRUPTED, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS.</p>

  <h2>9. Limitation of Liability</h2>
  <p>TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, CLUBHOUSE APPS SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR ANY PERSONAL INJURY OR PROPERTY DAMAGE, ARISING OUT OF OR IN CONNECTION WITH YOUR USE OF SOCCAR, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.</p>
  <p>Our total liability to you for any claims arising under these Terms shall not exceed the amount you paid us in the 12 months preceding the claim, or $10 USD, whichever is greater.</p>

  <h2>10. Indemnification</h2>
  <p>You agree to indemnify and hold harmless Clubhouse Apps from any claims, damages, losses, or expenses (including reasonable legal fees) arising from your use of SoccAR or your violation of these Terms.</p>

  <h2>11. Third-Party Services</h2>
  <p>SoccAR relies on services including Apple, Google, Supabase and Resend. Your use of those services is subject to their own terms and privacy policies.</p>

  <h2>12. Termination</h2>
  <p>You may stop using SoccAR and delete your account at any time. We may suspend or terminate your access for violation of these Terms. Sections that by their nature survive termination (including disclaimers and limitations of liability) remain in effect.</p>

  <h2>13. Governing Law</h2>
  <p>These Terms are governed by the laws of the State of Maine, United States, without regard to its conflict of law principles. Any disputes shall be resolved in the courts of Maine, and you consent to personal jurisdiction there.</p>

  <h2>14. Changes to Terms</h2>
  <p>We may update these Terms from time to time and will notify you of material changes within the app or by email. Your continued use of SoccAR after changes take effect means you accept the revised Terms.</p>

  <h2>15. Contact</h2>
  <p><strong>Clubhouse Apps</strong><br />
  Email: {MAIL}</p>'''

deletion = f'''          <p>You can delete your SoccAR account, and the personal data that goes with it, at any time.</p>

          <div class="callout">
            <p><strong>Account deletion is permanent and cannot be undone.</strong> Teams you created, and their drill history, cannot be recovered afterwards.</p>
          </div>

          <h2>What Gets Deleted</h2>
          <ul>
            <li>Your account, sign-in details and profile (name and email address)</li>
            <li>Every team you created, with its drill history and invite codes. Coaches you invited lose access to those teams.</li>
            <li>Your place on other coaches&rsquo; teams</li>
            <li>The teams and history stored on your iPhone, when you delete from within the app</li>
          </ul>
          <p>Drill entries you logged on a team another coach created stay in that team&rsquo;s history, because they are part of the team&rsquo;s record, but they are no longer linked to your account.</p>
          <p>Deletion from within the app happens immediately. Requests by email are processed within <strong>30 days</strong>. Backups containing your data are purged within 90 days.</p>

          <h2>How to Delete Your Account</h2>
          <div class="box">
            <h3>Option 1 — Delete from within the app</h3>
            <ol class="steps">
              <li>Open SoccAR on your iPhone and sign in</li>
              <li>Tap the team name at the top of the screen, then <strong>Account</strong></li>
              <li>Tap <strong>Delete Account</strong> and confirm</li>
            </ol>
          </div>

          <div class="box">
            <h3>Option 2 — Ask us by email</h3>
            <p>Email {MAIL} with the subject line <strong>"SoccAR Account Deletion"</strong> from the address on your account. We will confirm when deletion is complete.</p>
          </div>

          <h2>Questions</h2>
          <p>If you have questions about deleting your data, contact {MAIL}. See also our <a href="/soccar/privacy/">Privacy Policy</a>.</p>'''

page("soccar/", "SoccAR: drill cones in augmented reality: Clubhouse Apps",
     "SoccAR shows a soccer drill&rsquo;s cones on the real field through an iPhone camera. In beta on TestFlight.",
     "Lay out drills on the real field", None, landing)
page("soccar/privacy/", "SoccAR privacy policy: Clubhouse Apps",
     "What SoccAR collects, how it is used, and your rights over your data.", "Privacy policy", UPDATED, privacy)
page("soccar/terms/", "SoccAR terms of service: Clubhouse Apps",
     "The terms for using SoccAR, the augmented-reality drill app for soccer coaches.", "Terms of service", UPDATED, terms)
page("soccar/data-deletion/", "Delete your SoccAR data: Clubhouse Apps",
     "How to delete your SoccAR account and the data that goes with it, in the app or by email.",
     "Delete your data", UPDATED, deletion)
