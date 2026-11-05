# Notion template specs. Each template = a page with intro blocks and one or more databases.
# Property types follow the Notion API: title, rich_text, number, select, multi_select, status,
# date, checkbox, url, email, phone_number, formula, relation, rollup.
# build.py turns these into: Notion-import ZIPs (Markdown + CSV), preview images, and listings.
# create_in_notion.md explains how a session with the Notion connector builds them for real.

T = []

def db(name, icon, props, rows, views=None):
    return dict(name=name, icon=icon, props=props, rows=rows, views=views or ["Table"])

T.append(dict(slug="freelance-os", icon="💼", name="Freelance OS", price=19, accent="#2f6fed",
 tagline="Clients, projects, time, invoices and income in one Notion workspace",
 intro="Run your whole freelance business from one page. Add a client, start a project, log hours, send the invoice and watch your income dashboard update.",
 features=["Clients CRM with lead status and follow-up dates","Projects board from Lead to Paid, linked to clients","Time log with automatic billable amount","Invoices with due dates and automatic Overdue flag","Income by month and outstanding total via rollups","Weekly review checklist"],
 dbs=[
  db("Clients","👤",[("Name","title"),("Status","select",["Lead","Active","Past"]),("Email","email"),("Company","rich_text"),("Hourly rate","number"),("Next follow-up","date"),("Source","select",["Referral","Website","LinkedIn","Upwork","Cold email"])],
     [["Northwind Studio","Active","hello@northwind.example","Northwind","85","2026-11-12","Referral"],["Blue Fern Cafe","Lead","owner@bluefern.example","Blue Fern","70","2026-11-08","Website"],["Atlas Legal","Past","ops@atlas.example","Atlas LLP","95","","LinkedIn"]],["Table","Board by Status"]),
  db("Projects","📁",[("Project","title"),("Client","relation","Clients"),("Stage","status",["Lead","Proposal","In progress","Review","Done","Paid"]),("Value","number"),("Deadline","date"),("Priority","select",["High","Medium","Low"])],
     [["Website redesign","Northwind Studio","In progress","4200","2026-12-01","High"],["Menu & brand refresh","Blue Fern Cafe","Proposal","1500","2026-11-30","Medium"],["Contract templates","Atlas Legal","Paid","900","2026-10-10","Low"]],["Board by Stage","Calendar by Deadline","Table"]),
  db("Time log","⏱️",[("Task","title"),("Project","relation","Projects"),("Date","date"),("Hours","number"),("Rate","number"),("Billable","formula","prop(\"Hours\") * prop(\"Rate\")")],
     [["Wireframes","Website redesign","2026-11-03","3.5","85",""],["Client call","Website redesign","2026-11-04","1","85",""],["Logo concepts","Menu & brand refresh","2026-11-04","2","70",""]],["Table","Calendar by Date"]),
  db("Invoices","🧾",[("Invoice","title"),("Client","relation","Clients"),("Amount","number"),("Issued","date"),("Due","date"),("Paid","checkbox"),("Overdue","formula","if(not prop(\"Paid\") and dateBetween(now(), prop(\"Due\"), \"days\") > 0, \"⚠️ Overdue\", \"\")")],
     [["INV-001","Atlas Legal","900","2026-10-01","2026-10-15","Yes",""],["INV-002","Northwind Studio","2100","2026-10-20","2026-11-03","No",""],["INV-003","Northwind Studio","2100","2026-11-20","2026-12-04","No",""]],["Table","Unpaid","Board by Paid"]),
 ]))

T.append(dict(slug="personal-finance-dashboard", icon="💰", name="Personal Finance Dashboard", price=12, accent="#2b8a3e",
 tagline="Budget, transactions, savings goals and subscriptions in Notion",
 intro="Log what you spend, see each budget category fill up, and track savings goals and subscriptions from one dashboard.",
 features=["Transactions log with categories and month","Budget categories with spent-so-far rollups and remaining amount","Savings goals with progress bars","Subscriptions with monthly cost and renewal dates","Monthly view filtered to this month","Works on the free Notion plan"],
 dbs=[
  db("Transactions","💳",[("Description","title"),("Amount","number"),("Type","select",["Expense","Income"]),("Category","relation","Budget categories"),("Date","date"),("Account","select",["Checking","Credit card","Cash"])],
     [["Groceries","84.20","Expense","Food","2026-11-02","Credit card"],["Salary","3200","Income","Income","2026-11-01","Checking"],["Bus pass","45","Expense","Transport","2026-11-03","Checking"]],["Table","This month","By category"]),
  db("Budget categories","📊",[("Category","title"),("Monthly budget","number"),("Spent","rollup","Transactions.Amount sum"),("Remaining","formula","prop(\"Monthly budget\") - prop(\"Spent\")")],
     [["Food","450","",""],["Transport","120","",""],["Fun","150","",""],["Income","0","",""]],["Table","Gallery"]),
  db("Savings goals","🎯",[("Goal","title"),("Target","number"),("Saved","number"),("Progress","formula","round(prop(\"Saved\") / prop(\"Target\") * 100) / 100"),("By","date")],
     [["Emergency fund","5000","1800","","2027-06-30"],["Holiday","1500","600","","2027-07-01"]],["Gallery","Table"]),
  db("Subscriptions","🔁",[("Service","title"),("Cost","number"),("Billing","select",["Monthly","Yearly"]),("Per month","formula","if(prop(\"Billing\") == \"Yearly\", round(prop(\"Cost\") / 12 * 100) / 100, prop(\"Cost\"))"),("Renews","date"),("Cancel?","checkbox")],
     [["Netflix","15.49","Monthly","","2026-11-14","No"],["Adobe CC","659","Yearly","","2027-02-01","No"],["Gym","35","Monthly","","2026-11-20","Yes"]],["Table"]),
 ]))

T.append(dict(slug="habit-goal-tracker", icon="✅", name="Habit & Goal Tracker", price=7, accent="#7048e8",
 tagline="Daily habit check-ins, streak-friendly views and goals with progress",
 intro="Tick your habits each day, see your weekly completion rate, and connect habits to the bigger goals they move forward.",
 features=["Daily log with one checkbox per habit","Automatic daily score (habits done / total)","Goals with milestones and progress","Weekly and monthly views","Reflection prompts page"],
 dbs=[
  db("Daily log","📅",[("Day","title"),("Date","date"),("Workout","checkbox"),("Read 20 min","checkbox"),("Drink 2L water","checkbox"),("No phone after 10pm","checkbox"),("Meditate","checkbox"),("Score","formula","round(((if(prop(\"Workout\"),1,0)+if(prop(\"Read 20 min\"),1,0)+if(prop(\"Drink 2L water\"),1,0)+if(prop(\"No phone after 10pm\"),1,0)+if(prop(\"Meditate\"),1,0))/5)*100)/100")],
     [["Mon","2026-11-02","Yes","Yes","No","Yes","No",""],["Tue","2026-11-03","No","Yes","Yes","Yes","Yes",""],["Wed","2026-11-04","Yes","No","Yes","No","Yes",""]],["Table","This week","Calendar"]),
  db("Goals","🏔️",[("Goal","title"),("Area","select",["Health","Career","Money","Learning","Relationships"]),("Status","status",["Not started","In progress","Done"]),("Progress","number"),("Target date","date"),("Why it matters","rich_text")],
     [["Run a 10K","Health","In progress","0.4","2027-04-01","Feel fit and confident"],["Read 24 books","Learning","In progress","0.25","2027-12-31","Learn every day"],["Save 3 months expenses","Money","Not started","0","2027-09-01","Peace of mind"]],["Board by Status","Gallery"]),
 ]))

T.append(dict(slug="content-calendar", icon="📣", name="Content Creator Planner", price=12, accent="#e64980",
 tagline="Ideas, content calendar, sponsors and stats for YouTube, TikTok and Instagram",
 intro="Capture ideas, move them through scripting, filming and editing, schedule posts on a calendar and keep sponsor deals in one place.",
 features=["Ideas bank with hook and platform","Content pipeline board: Idea to Published","Publishing calendar","Sponsor deals with fee, deliverables and paid status","Post stats: views, likes and engagement rate formula","Caption and hashtag snippets page"],
 dbs=[
  db("Content","🎬",[("Title","title"),("Platform","multi_select",["YouTube","TikTok","Instagram","LinkedIn","Blog"]),("Stage","status",["Idea","Scripting","Filming","Editing","Scheduled","Published"]),("Publish date","date"),("Format","select",["Long video","Short","Carousel","Post","Story"]),("Hook","rich_text"),("Views","number"),("Likes","number"),("Engagement","formula","if(prop(\"Views\") > 0, round(prop(\"Likes\") / prop(\"Views\") * 1000) / 1000, 0)")],
     [["5 budgeting mistakes","YouTube","Editing","2026-11-10","Long video","I wasted $3k before I learned this","",""],["Desk setup tour","TikTok","Published","2026-11-01","Short","My $200 desk setup","12400","980",""],["Notion for beginners","Instagram","Idea","","Carousel","Stop using 5 apps","",""]],["Board by Stage","Calendar by Publish date","Table"]),
  db("Sponsors","🤝",[("Brand","title"),("Fee","number"),("Deliverables","rich_text"),("Due","date"),("Status","select",["Pitched","Negotiating","Signed","Delivered","Paid"]),("Contact","email")],
     [["Acme VPN","650","1 integration (60s)","2026-11-20","Signed","partners@acme.example"],["Sprout Coffee","300","3 stories","2026-12-01","Negotiating","hi@sprout.example"]],["Board by Status","Table"]),
 ]))

T.append(dict(slug="student-planner", icon="🎓", name="Student Planner", price=9, accent="#0b7285",
 tagline="Courses, assignments, exams and grades for high school and university",
 intro="Every class, assignment and exam in one place, with days-left countdowns and a grade average per course.",
 features=["Courses with teacher, room and schedule","Assignments with due date, status and days-left formula","Exams with study checklist","Grade average per course via rollup","This week view and calendar"],
 dbs=[
  db("Courses","📚",[("Course","title"),("Teacher","rich_text"),("Room","rich_text"),("Days","multi_select",["Mon","Tue","Wed","Thu","Fri"]),("Average","rollup","Assignments.Grade average")],
     [["Biology","Dr. Reyes","B12","Mon, Wed",""],["History","Mr. Okafor","A4","Tue, Thu",""],["Maths","Ms. Lind","C2","Mon, Wed, Fri",""]],["Gallery","Table"]),
  db("Assignments","📝",[("Assignment","title"),("Course","relation","Courses"),("Due","date"),("Status","status",["To do","In progress","Submitted","Graded"]),("Grade","number"),("Weight","number"),("Days left","formula","if(prop(\"Status\") == \"Submitted\" or prop(\"Status\") == \"Graded\", \"\", format(dateBetween(prop(\"Due\"), now(), \"days\")) + \" days\")")],
     [["Lab report: enzymes","Biology","2026-11-12","In progress","","0.2",""],["Essay: Industrial Revolution","History","2026-11-18","To do","","0.3",""],["Problem set 4","Maths","2026-11-02","Graded","88","0.1",""]],["Board by Status","Calendar by Due","This week"]),
  db("Exams","⏰",[("Exam","title"),("Course","relation","Courses"),("Date","date"),("Topics","rich_text"),("Ready","checkbox")],
     [["Biology midterm","Biology","2026-11-25","Cells, enzymes, genetics","No"],["Maths quiz","Maths","2026-11-14","Quadratics","No"]],["Table","Calendar"]),
 ]))

T.append(dict(slug="job-search-tracker", icon="🧭", name="Job Search Tracker", price=7, accent="#e8590c",
 tagline="Applications pipeline, contacts, interviews and follow-ups",
 intro="Track every application from wishlist to offer, prepare for interviews and never miss a follow-up.",
 features=["Applications board: Wishlist to Offer","Follow-up date with automatic 'Follow up now' flag","Contacts and referrals linked to companies","Interview log with questions and notes","Salary range and location fields","STAR answers page for interview prep"],
 dbs=[
  db("Applications","📨",[("Role","title"),("Company","rich_text"),("Stage","status",["Wishlist","Applied","Interview","Offer","Rejected"]),("Applied on","date"),("Follow up","date"),("Salary range","rich_text"),("Link","url"),("Flag","formula","if(prop(\"Stage\") == \"Applied\" and dateBetween(now(), prop(\"Follow up\"), \"days\") >= 0, \"🔔 Follow up now\", \"\")")],
     [["Product Designer","Lumen","Interview","2026-10-28","2026-11-06","70-80k","https://example.com/jobs/1",""],["UX Researcher","Kite","Applied","2026-11-01","2026-11-08","65-75k","https://example.com/jobs/2",""],["Design Lead","Orbit","Wishlist","","","90k+","https://example.com/jobs/3",""]],["Board by Stage","Table"]),
  db("Contacts","📇",[("Name","title"),("Company","rich_text"),("Role","rich_text"),("Email","email"),("Last contact","date"),("Notes","rich_text")],
     [["Priya N.","Lumen","Hiring manager","priya@lumen.example","2026-11-02","Liked my case study"],["Tom B.","Kite","Recruiter","tom@kite.example","2026-11-01","Call next week"]],["Table"]),
  db("Interviews","🎤",[("Interview","title"),("Application","relation","Applications"),("Date","date"),("Type","select",["Phone screen","Technical","Portfolio","Final"]),("Questions asked","rich_text"),("Went well","checkbox")],
     [["Lumen: portfolio review","Product Designer","2026-11-07","Portfolio","",""]],["Table","Calendar"]),
 ]))

T.append(dict(slug="reading-tracker", icon="📖", name="Reading Tracker & Book Journal", price=5, accent="#8f5b34",
 tagline="Bookshelf gallery, reading goals, ratings, quotes and TBR list",
 intro="A cosy book journal in Notion: a bookshelf gallery, star ratings, favourite quotes and a yearly reading goal.",
 features=["Bookshelf gallery with covers","Status: TBR, Reading, Finished, DNF","Star rating, genre and pages","Quotes linked to books","Yearly goal progress","Reading challenge ideas page"],
 dbs=[
  db("Books","📚",[("Title","title"),("Author","rich_text"),("Status","status",["TBR","Reading","Finished","DNF"]),("Rating","select",["⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"]),("Genre","multi_select",["Fiction","Fantasy","Romance","Mystery","Non-fiction","Self-help"]),("Pages","number"),("Finished","date")],
     [["The Midnight Library","Matt Haig","Finished","⭐⭐⭐⭐","Fiction","304","2026-10-20"],["Atomic Habits","James Clear","Reading","","Self-help","320",""],["Project Hail Mary","Andy Weir","TBR","","Fiction","496",""]],["Gallery (bookshelf)","Board by Status","Table"]),
  db("Quotes","💬",[("Quote","title"),("Book","relation","Books"),("Page","number")],
     [["Between life and death there is a library.","The Midnight Library","1"]],["Table"]),
 ]))

T.append(dict(slug="meal-planner-recipes", icon="🥗", name="Meal Planner & Recipe Book", price=7, accent="#5c940d",
 tagline="Recipe database, weekly meal plan and grocery list",
 intro="Save your recipes once, drag them into the week, and build your grocery list in minutes.",
 features=["Recipe book gallery with tags, time and servings","Weekly meal plan linked to recipes","Grocery list grouped by aisle with checkboxes","Filter: quick meals under 30 minutes","Pantry staples list"],
 dbs=[
  db("Recipes","🍲",[("Recipe","title"),("Meal","multi_select",["Breakfast","Lunch","Dinner","Snack"]),("Minutes","number"),("Servings","number"),("Tags","multi_select",["Vegetarian","High protein","Budget","Meal prep"]),("Ingredients","rich_text"),("Link","url")],
     [["Overnight oats","Breakfast","5","1","Vegetarian, Meal prep","Oats, milk, chia, berries",""],["Chicken stir fry","Dinner","25","2","High protein","Chicken, peppers, soy, rice",""],["Lentil soup","Lunch, Dinner","40","4","Vegetarian, Budget","Lentils, carrot, onion, stock",""]],["Gallery","Quick meals","Table"]),
  db("Meal plan","🗓️",[("Day","title"),("Date","date"),("Breakfast","relation","Recipes"),("Lunch","relation","Recipes"),("Dinner","relation","Recipes")],
     [["Monday","2026-11-09","Overnight oats","Lentil soup","Chicken stir fry"],["Tuesday","2026-11-10","Overnight oats","Lentil soup",""]],["Table","Calendar"]),
  db("Grocery list","🛒",[("Item","title"),("Aisle","select",["Produce","Dairy","Meat","Pantry","Frozen","Other"]),("Qty","rich_text"),("Got it","checkbox")],
     [["Oats","Pantry","1 bag","No"],["Berries","Produce","2 packs","No"],["Chicken breast","Meat","500 g","No"]],["Board by Aisle","Table"]),
 ]))

BUNDLE = dict(slug="notion-life-os-bundle", name="Notion Life & Business Bundle", price=39, accent="#212529",
 items=[t["slug"] for t in T],
 tagline="All 8 Notion templates: freelance, finance, habits, content, study, job search, reading and meals")
