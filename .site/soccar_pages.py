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

UPDATED = "November 27, 2026"

landing = f'''  <p class="t-lead">SoccAR keeps a youth soccer team organized: the schedule, who&rsquo;s coming, team messages and the league table, in one app for coaches, the team manager, parents and players. Coaches also get augmented-reality drill layouts on the real field.</p>

  <h2>For the whole team</h2>
  <ul>
    <li><strong>One schedule.</strong> Practices, games and team events with times, fields and directions. Families can add it to the calendar on their phone, and it updates by itself when something changes.</li>
    <li><strong>Changes reach everyone.</strong> When a coach moves a practice, changes a field or cancels a game, parents and players get a notification right away.</li>
    <li><strong>Who&rsquo;s coming.</strong> Parents mark whether their child is going, can&rsquo;t go, or might, with a note for the coach. Coaches see the count for every practice and game.</li>
    <li><strong>News and announcements.</strong> Coaches post to parents, players or both, with photos if they like. Parents can heart and comment, and everyone gets a push notification.</li>
    <li><strong>Team chat.</strong> Coaches and parents talk in one team chat (photos welcome); coaches have their own. Before a game, the two teams&rsquo; coaches can message each other.</li>
    <li><strong>Carpools and comments.</strong> Offer a ride or book a seat for your child, and ask a question right on a practice or game.</li>
    <li><strong>Game day.</strong> Coaches share the lineup and keep a live score with goals, cards and subs, so families at home can follow along.</li>
    <li><strong>Every team in one place.</strong> Kids on more than one team? See every schedule together, and tap a notification to land on exactly what it&rsquo;s about. Answer &ldquo;Going&rdquo; or &ldquo;Can&rsquo;t go&rdquo; right from the notification.</li>
    <li><strong>Leagues and standings.</strong> Start a league or join one with a code, or import your league&rsquo;s calendar link. Final scores build the table automatically.</li>
  </ul>

  <h2>For coaches</h2>
  <ul>
    <li><strong>Drills on the real field.</strong> Pick one of more than 30 layouts, aim the camera at the grass and tap. The cones appear life-size where you aimed, with distances in yards.</li>
    <li><strong>Season plan.</strong> Attach drills and your own exercises to each practice, then run the plan on the field drill by drill.</li>
    <li><strong>Drill history and co-coaches.</strong> See what each team ran and when. Invite assistant coaches, and the head coach can name a team manager who can also run the schedule.</li>
  </ul>

  <h2>Built for kids&rsquo; teams</h2>
  <p>Photos are always optional and private to the team they&rsquo;re posted to: nobody outside the team can see them. SoccAR never asks for birthdays or players&rsquo; contact details; the roster is names and jersey numbers, with an optional photo. Players can see the schedule, news and standings but cannot message anyone. Players under 13 don&rsquo;t get their own account; their parents see everything they need.</p>

  <h2>How to get it</h2>
  <p>SoccAR is in a private beta on TestFlight for iPhone. The drill camera needs an iPhone that supports ARKit (an iPhone XS or later). Families on Android can subscribe to the team calendar in Google Calendar. To ask about the beta, email {MAIL}.</p>

  <h2>Help</h2>
  <ul>
    <li><a href="/soccar/account/">Account help</a>: password resets and email links</li>
    <li><a href="/soccar/data-deletion/">Delete your data</a></li>
    <li><a href="/soccar/privacy/">Privacy policy</a> and <a href="/soccar/terms/">Terms of service</a></li>
  </ul>'''

privacy = f'''  <p>Clubhouse Apps ("we," "our," or "us") operates the SoccAR iOS application and the ClubhouseApps.com website. This Privacy Policy explains what information SoccAR collects, how we use it, who can see it, and your rights regarding your data. SoccAR is used by coaches, team managers, parents and players of youth soccer teams, so this policy also explains how we handle information about children.</p>
  <p>By using SoccAR, you agree to the practices described in this policy. If you do not agree, please do not use the app.</p>

  <h2>1. Information We Collect</h2>
  <p><strong>Account information:</strong> When you create an account, we collect your email address and, if you sign in with Apple or Google, your name (if you choose to share it). If you sign up with an email address and password, your password is stored by our authentication provider in hashed form; we never see it.</p>
  <p><strong>Teams and roles:</strong> We store the names of teams, who belongs to each team and their role (head coach, assistant coach, team manager, parent or player), and the invite codes used to join, including when each code expires and which account used it.</p>
  <p><strong>Team roster:</strong> Coaches and the team manager may enter each player&rsquo;s first name, last name or initial, and jersey number, and we record which parent accounts are linked to which player. A player&rsquo;s photo may be added by the team&rsquo;s staff, the player&rsquo;s parent, or the player; it is optional. SoccAR does not ask for, and we ask you not to enter, players&rsquo; birth dates, addresses, phone numbers or email addresses.</p>
  <p><strong>Photos:</strong> Coaches may add photos to news posts, coaches and parents may share photos in team chat, and a player&rsquo;s photo may be added to the roster. Photos are always optional. They are stored privately and only members of the team they were posted to can see them (chat photos: only the people in that chat). Before upload, SoccAR shrinks each photo and removes its hidden details, such as where it was taken.</p>
  <p><strong>Schedule and availability:</strong> Practices, games and team events (times, places, addresses and notes), saved fields, game scores, lineups, goals, cards and substitutions entered during games (with the player&rsquo;s first name for our own team), and the answers parents and players give about whether a player is coming, with any note they add. If a coach imports a league calendar link, we store the link and copy the games and events in it onto that team&rsquo;s schedule.</p>
  <p><strong>Carpools and comments:</strong> Rides parents offer (direction, seats and a note) and which children are riding, and comments on news posts, practices and games, with hearts on posts.</p>
  <p><strong>Contact details you choose to share:</strong> If you switch on sharing, the phone number and email address you enter for a team. Nothing is shared unless you turn it on, and you can turn it off at any time.</p>
  <p><strong>Team email:</strong> When a coach or the team manager emails the team, we keep a copy of the message and how many people it went to.</p>
  <p><strong>Leagues:</strong> League names, the teams in each league, league codes, and game results used to build standings.</p>
  <p><strong>Messages:</strong> Announcements, team chat and coaches&rsquo; chat messages (including any photos), and the time each was sent. If you report a message, post, comment or photo, we store the report and the reason. If you block someone, we store that so their messages stay hidden from you.</p>
  <p><strong>Notifications:</strong> If you allow notifications, we store your iPhone&rsquo;s push notification token so we can send you team updates, a list of the notifications we sent you and whether you have read them, and the notification settings you choose for each team.</p>
  <p><strong>Drill plans and history:</strong> The drills and exercises coaches plan for practices, and which drills a team ran on which day.</p>
  <p><strong>Camera and photo library:</strong> SoccAR uses your iPhone&rsquo;s camera and motion sensors in the coaches&rsquo; drill screen, to find the ground and show cones on it. This is processed on your iPhone by Apple&rsquo;s ARKit; we do not record or upload those camera images. When you choose to post a photo, you pick it from your photo library and only that photo is uploaded. When you tap Save to Photos, SoccAR adds that photo to your library.</p>
  <p><strong>Information kept on your iPhone:</strong> A copy of your teams, schedule, roster, announcements and drill history is stored on your iPhone so the app works without a signal. Your chosen drill, cone color and other settings stay on your iPhone.</p>
  <p><strong>Device and usage information:</strong> SoccAR contains no advertising, no third-party analytics, and no crash-reporting tools. We do not collect location data; addresses you see are ones a coach typed in. If you install SoccAR through TestFlight, Apple may share crash reports and feedback you choose to send with us, under Apple&rsquo;s terms.</p>

  <h2>2. How We Use Your Information</h2>
  <ul>
    <li>To create and secure your account and sign you in</li>
    <li>To show each team&rsquo;s schedule, roster, messages and standings to the people on that team</li>
    <li>To send push notifications about news, schedule changes, comments, lineups, goals and game results, and messages</li>
    <li>To send team emails that a coach or the team manager writes</li>
    <li>To import a league calendar that a coach links</li>
    <li>To provide a private calendar feed of the team schedule</li>
    <li>To review reported messages and enforce our Terms</li>
    <li>To send service emails, such as confirming your email address and resetting your password (never marketing without your consent)</li>
    <li>To respond to you when you contact us for support</li>
  </ul>

  <h2>3. Third-Party Services</h2>
  <p>We share data with the following third parties to operate SoccAR:</p>
  <ul>
    <li><strong>Supabase</strong> — Cloud database, private photo storage, authentication and server functions. Stores the information described above. Hosted in the United States.</li>
    <li><strong>Apple Push Notification service</strong> — Delivers notifications to your iPhone. Apple receives your device token and the text of each notification.</li>
    <li><strong>Resend</strong> — Sends account emails (email confirmation and password reset) and team emails written by your team&rsquo;s coaches or manager.</li>
    <li><strong>Apple Sign-In</strong> — Optional sign-in method. Governed by Apple&rsquo;s Privacy Policy.</li>
    <li><strong>Google Sign-In</strong> — Optional sign-in method. Governed by Google&rsquo;s Privacy Policy.</li>
    <li><strong>Apple TestFlight</strong> — Distributes the beta app. Governed by Apple&rsquo;s terms and privacy policy.</li>
    <li><strong>Cloudflare and GitHub Pages</strong> — Serve this website.</li>
  </ul>
  <p>If you subscribe to a team calendar, the calendar app you use (for example Apple Calendar or Google Calendar) fetches the schedule from us and handles it under its own privacy policy.</p>
  <p>We do not sell your personal data to any third party, and we do not use it for advertising.</p>

  <h2>4. Who Can See Your Information</h2>
  <ul>
    <li><strong>Coaches and the team manager</strong> see everything about their team: the roster and player photos, which parents are linked to which player, the schedule, everyone&rsquo;s availability answers, news, comments, carpools, the team chat and coaches&rsquo; chat, lineups, drill plans and drill history.</li>
    <li><strong>Parents</strong> see the roster and player photos, the schedule, their own children&rsquo;s availability answers (and everyone&rsquo;s, if the coaches turn that on), news sent to parents, comments, carpools, published lineups, live scores, the team chat, shared contact details and standings. They cannot see drill plans or the coaches&rsquo; chat.</li>
    <li><strong>Players</strong> see the schedule, the roster and player photos, news sent to players, published lineups, live scores and standings. They cannot see or send messages, comments or contact details.</li>
    <li><strong>Another team&rsquo;s coaches and families</strong> see a game you are playing against them (time, place, score, and when goals, cards and subs happened, but not your players&rsquo; names), and the opposing coaches see that game&rsquo;s coaches-only chat. They see nothing else about your team, including its photos.</li>
    <li><strong>League members</strong> see the league&rsquo;s team names, its games and its standings.</li>
    <li><strong>Anyone with your team&rsquo;s calendar link</strong> can see the team schedule (times, places and notes, but no names of players). Share it only within the team.</li>
  </ul>
  <p>Your name and email address are visible to the other members of your teams. Anyone with a valid invite code can join a team until the code is used or expires, so share codes only with the person they are meant for.</p>

  <h2>5. Data Retention</h2>
  <p>We keep team information for as long as the team exists, and your account information for as long as your account is active. You can delete your account at any time (see Section 9). Unused invite codes expire after 7 days.</p>

  <h2>6. Children&rsquo;s Privacy (COPPA)</h2>
  <p>SoccAR is used to organize children&rsquo;s sports teams, so we limit what we collect about children:</p>
  <ul>
    <li>Children under 13 may not create an account. Information about a player under 13 is limited to the first name, last name or initial, and jersey number a coach enters on the roster, and the attendance answers their parent gives. We use it only to run the team, and only that team&rsquo;s members can see it.</li>
    <li>Players aged 13 to 17 may be invited by a coach to a view-only account. These accounts cannot send messages, and we collect only the account information described in Section 1.</li>
    <li>We never ask for players&rsquo; birth dates or contact details. Photos are optional and only visible to the player&rsquo;s own team. A parent may remove their child&rsquo;s player photo in the app at any time, or ask the coach or us to remove any photo of their child.</li>
  </ul>
  <p>A parent may ask to see, correct or delete information about their child at any time by asking the team&rsquo;s coach or by emailing {MAIL}. If you believe we have collected information from a child under 13 without a parent&rsquo;s knowledge, contact us and we will delete it.</p>

  <h2>7. Your Rights — GDPR (European Users)</h2>
  <p>If you are located in the European Economic Area, you have the right to access, correct, delete, and receive a portable copy of your personal data, and to object to certain processing. To exercise any of these rights, email us at {MAIL}. We will respond within 30 days.</p>

  <h2>8. Your Rights — CCPA (California Users)</h2>
  <p>If you are a California resident, you have the right to know what personal information we collect, the right to request deletion, and the right to opt out of the sale of your personal information. <strong>We do not sell your personal information.</strong> To exercise your rights, contact us at {MAIL}.</p>

  <h2>9. Account and Data Deletion</h2>
  <p>You can delete your SoccAR account from within the app, or by emailing {MAIL}. Deleting your account permanently removes your profile, the teams you created (with their roster, schedule, messages and history), the leagues you organize, your place on other teams, your shared contact details, your notification tokens and settings, and your blocks and reports. Photos stored for teams you started are deleted too. Messages, photos, comments, announcements and drill entries you posted on teams you did not create stay with those teams, because they are part of the team&rsquo;s record, but they are no longer linked to your name. You can delete your own messages, comments and photos in the app before deleting your account. For details, see our <a href="/soccar/data-deletion/">Data Deletion page</a>.</p>

  <h2>10. Cookies and Tracking (Website)</h2>
  <p>The SoccAR pages on ClubhouseApps.com use no advertising cookies or third-party tracking scripts. Cloudflare may set cookies for security and performance purposes. The email confirmation, account and join pages contact Supabase only when you tap a button on them. When a coach imports a calendar link, our server fetches that link; the site it comes from sees a request from our server, not from you.</p>

  <h2>11. Security</h2>
  <p>We use encrypted connections (TLS), row-level security on our database so each person can reach only the teams they belong to and only what their role allows, and token-based authentication. No method of transmission over the internet is 100% secure, but we take reasonable precautions to protect your data.</p>

  <h2>12. Changes to This Policy</h2>
  <p>We may update this Privacy Policy from time to time. When we do, we will update the "Last updated" date at the top of this page, and for material changes we will notify you within the app. Your continued use of SoccAR after changes are posted means you accept the revised policy.</p>

  <h2>13. Contact Us</h2>
  <p><strong>Clubhouse Apps</strong><br />
  Email: {MAIL}<br />
  Website: <a href="https://clubhouseapps.com">clubhouseapps.com</a></p>'''

terms = f'''  <p>These Terms of Service ("Terms") govern your use of SoccAR, provided by Clubhouse Apps ("we," "our," or "us"). By downloading or using SoccAR, you agree to these Terms. If you do not agree, do not use the app.</p>

  <h2>1. Description of Service</h2>
  <p>SoccAR is an iOS application for organizing youth soccer teams. It includes a team schedule with a calendar feed and calendar import, attendance, carpools, news with optional photos, comments, team email, announcements and push notifications, team and coaches&rsquo; chat, lineups and live scoring, leagues and standings, and, for coaches, practice planning, drill history and augmented-reality drill layouts on a real field. SoccAR is currently offered free of charge as a beta through Apple&rsquo;s TestFlight.</p>

  <h2>2. Beta Software</h2>
  <p>SoccAR is pre-release software. Features may change, stop working, or be removed, and data may be lost. Notifications may arrive late or not at all. <strong>Do not rely on SoccAR as the only way to tell families about urgent changes, such as a game cancelled for weather or a safety issue.</strong> Beta builds expire on the schedule Apple sets for TestFlight.</p>

  <h2>3. Eligibility and Roles</h2>
  <ul>
    <li>You must be at least 18 years old, or the age of majority where you live, to create a coach, team manager or parent account, or to start a team or league.</li>
    <li>Players aged 13 to 17 may use a view-only player account if a coach invites them, with their parent&rsquo;s permission. Children under 13 may not create an account.</li>
    <li>The coach who starts a team is its head coach. The head coach decides who is an assistant coach, team manager or parent, and can remove anyone from the team.</li>
  </ul>

  <h2>4. Accounts, Teams and Invite Codes</h2>
  <p>You are responsible for keeping your sign-in details private and for all activity under your account. Notify us at {MAIL} if you suspect unauthorized access.</p>
  <p>Coaches and team managers are responsible for who they invite. Give each invite code only to the person it is for; a code links a parent to a specific player. Keep the team calendar link within the team.</p>
  <p>If you add players to a roster, you confirm that you are entitled to do so for your team (for example, as its coach or manager) and you will enter only names or initials and jersey numbers, not birth dates or contact details.</p>
  <p><strong>Photos.</strong> Photos are optional. Post only photos you have the right to share and that the families of any children shown are comfortable with; remove a photo of a child if their parent asks. Never post photos that show a child undressed, in a changing area, in distress, or with personal details such as a school name or home address. We may remove any photo and suspend accounts that misuse photos.</p>
  <p><strong>Calendar import.</strong> Import only a calendar link you are allowed to use for your own team, such as one your league or club gives you. You are responsible for following that site&rsquo;s terms.</p>
  <p><strong>Contact details and email.</strong> Contact details others share with the team are for team matters only. Team email is for team business; don&rsquo;t use it for advertising or anything unrelated to the team.</p>

  <h2>5. Messages and Conduct</h2>
  <p>Announcements and chats are for running the team. When you post, you agree to:</p>
  <ul>
    <li>Be respectful. No harassment, bullying, threats, hate speech, sexual content, or content that is illegal or harmful.</li>
    <li>Never post anything that sexualizes, endangers or exploits a child, or that shares a child&rsquo;s personal information beyond what the team needs.</li>
    <li>Not use SoccAR to contact players privately. SoccAR does not allow messages to or from players.</li>
    <li>Not post spam, advertising, or other people&rsquo;s private information.</li>
    <li>Not post photos of other families&rsquo; children against their wishes.</li>
  </ul>
  <p>You can report any message, post, comment or photo from inside the app and block anyone&rsquo;s messages. We review reports, may remove messages that break these Terms, and may suspend or remove accounts that do. Where the law requires it, or where a child may be at risk, we may report content to the authorities.</p>

  <h2>6. Safety on the Field</h2>
  <p><strong>Watch where you are going.</strong> Do not walk or run while looking at your screen near players, balls, goals, traffic, water or other hazards. Stay aware of your surroundings at all times.</p>
  <p><strong>Placement is approximate.</strong> Augmented reality tracking can drift, especially over long distances, on plain or uneven ground, or in poor light. Cone positions and distances shown in the app are estimates. Check measurements yourself when they matter.</p>
  <p><strong>Drills are for guidance only.</strong> The drill layouts are general examples. You are responsible for choosing activities that are safe and suitable for your players&rsquo; ages, abilities and conditions, and for following the rules of your club, league and governing body.</p>
  <p><strong>Schedules and standings come from users.</strong> Times, places and scores are entered by coaches, team managers and league organizers. We do not check them. Standings in SoccAR are not official unless your league says they are.</p>

  <h2>7. Acceptable Use</h2>
  <p>You agree not to:</p>
  <ul>
    <li>Use SoccAR for any unlawful purpose</li>
    <li>Attempt to reverse engineer, decompile, or extract the source code of the app</li>
    <li>Use automated tools to access the app or its servers</li>
    <li>Access, or try to access, teams, leagues or accounts that are not yours</li>
    <li>Impersonate anyone, or join a team as a parent of a child who is not yours</li>
  </ul>

  <h2>8. Intellectual Property</h2>
  <p>SoccAR, its design, code, branding, and drill library are the property of Clubhouse Apps and protected by applicable intellectual property laws. You are granted a limited, non-exclusive, non-transferable license to use the app to organize and coach your team. Content you create (team names, schedules, messages, plans and history) remains yours; you grant us a limited license to store, process and show it to the people on your team, league or game, as described in our Privacy Policy, to provide the service.</p>

  <h2>9. Disclaimers</h2>
  <p>SOCCAR IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SERVICE, INCLUDING NOTIFICATIONS, WILL BE UNINTERRUPTED, TIMELY, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS. WE ARE NOT RESPONSIBLE FOR CONTENT POSTED BY USERS.</p>

  <h2>10. Limitation of Liability</h2>
  <p>TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, CLUBHOUSE APPS SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR ANY PERSONAL INJURY OR PROPERTY DAMAGE, ARISING OUT OF OR IN CONNECTION WITH YOUR USE OF SOCCAR, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.</p>
  <p>Our total liability to you for any claims arising under these Terms shall not exceed the amount you paid us in the 12 months preceding the claim, or $10 USD, whichever is greater.</p>

  <h2>11. Indemnification</h2>
  <p>You agree to indemnify and hold harmless Clubhouse Apps from any claims, damages, losses, or expenses (including reasonable legal fees) arising from your use of SoccAR, the content you post, or your violation of these Terms.</p>

  <h2>12. Third-Party Services</h2>
  <p>SoccAR relies on services including Apple, Google, Supabase and Resend. Your use of those services is subject to their own terms and privacy policies.</p>

  <h2>13. Termination</h2>
  <p>You may stop using SoccAR and delete your account at any time. We may suspend or terminate your access for violation of these Terms. Sections that by their nature survive termination (including disclaimers and limitations of liability) remain in effect.</p>

  <h2>14. Governing Law</h2>
  <p>These Terms are governed by the laws of the State of Maine, United States, without regard to its conflict of law principles. Any disputes shall be resolved in the courts of Maine, and you consent to personal jurisdiction there.</p>

  <h2>15. Changes to Terms</h2>
  <p>We may update these Terms from time to time and will notify you of material changes within the app or by email. Your continued use of SoccAR after changes take effect means you accept the revised Terms.</p>

  <h2>16. Contact</h2>
  <p><strong>Clubhouse Apps</strong><br />
  Email: {MAIL}</p>'''

deletion = f'''          <p>You can delete your SoccAR account, and the personal data that goes with it, at any time.</p>

          <div class="callout">
            <p><strong>Account deletion is permanent and cannot be undone.</strong> Teams you started, with their roster, schedule, messages and history, cannot be recovered afterwards.</p>
          </div>

          <h2>What Gets Deleted</h2>
          <ul>
            <li>Your account, sign-in details and profile (name and email address)</li>
            <li>Every team you started as head coach, with its roster, photos, schedule, availability, carpools, comments, news, chats, lineups and scores, drill plans, drill history and invite codes. Everyone else on those teams loses access to them.</li>
            <li>Leagues you organize</li>
            <li>Your place on other teams, and your links to players as a parent</li>
            <li>Your shared contact details, notification tokens, notifications and settings, and the blocks and reports you made</li>
            <li>The copy of your teams stored on your iPhone, when you delete from within the app</li>
          </ul>
          <p>Messages, photos, comments, announcements, attendance answers and drill entries you posted on teams someone else started stay with those teams, because they are part of the team&rsquo;s record, but they are no longer linked to your name. You can delete your own messages, comments and photos in the app first.</p>
          <p><strong>Parents:</strong> you can remove your child&rsquo;s player photo yourself (Team → tap your child → Remove photo). To remove your child from a team&rsquo;s roster, or any other photo of your child, ask the team&rsquo;s coach, or email us and we will remove it.</p>
          <p>Deletion from within the app happens immediately. Requests by email are processed within <strong>30 days</strong>. Backups containing your data are purged within 90 days.</p>

          <h2>How to Delete Your Account</h2>
          <div class="box">
            <h3>Option 1 — Delete from within the app</h3>
            <ol class="steps">
              <li>Open SoccAR on your iPhone and sign in</li>
              <li>Tap the person icon at the top right of Home to open <strong>Account</strong></li>
              <li>Tap <strong>Delete Account</strong> and confirm</li>
            </ol>
          </div>

          <div class="box">
            <h3>Option 2 — Ask us by email</h3>
            <p>Email {MAIL} with the subject line <strong>"SoccAR Account Deletion"</strong> from the address on your account. We will confirm when deletion is complete.</p>
          </div>

          <h2>Questions</h2>
          <p>If you have questions about deleting your data, contact {MAIL}. See also our <a href="/soccar/privacy/">Privacy Policy</a>.</p>'''

page("soccar/", "SoccAR: the youth soccer team app: Clubhouse Apps",
     "SoccAR keeps a youth soccer team organized: schedule, attendance, team messages and standings, with AR drill layouts for coaches. In beta on TestFlight.",
     "Your soccer team, organized", None, landing)
page("soccar/privacy/", "SoccAR privacy policy: Clubhouse Apps",
     "What SoccAR collects, how it is used, and your rights over your data.", "Privacy policy", UPDATED, privacy)
page("soccar/terms/", "SoccAR terms of service: Clubhouse Apps",
     "The terms for using SoccAR, the team app for youth soccer coaches, parents and players.", "Terms of service", UPDATED, terms)
page("soccar/data-deletion/", "Delete your SoccAR data: Clubhouse Apps",
     "How to delete your SoccAR account and the data that goes with it, in the app or by email.",
     "Delete your data", UPDATED, deletion)
