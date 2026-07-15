import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests 
import uuid
load_dotenv()



clean_bullets=[{"text":"Developed a log analyzer Python automation script to parse and categorize captured error messages, generating individual output files for each error type, enabling faster identification and resolution of system issues.","source_id":["EXP-CGI-1"]},
               {"text":"Utilized strong foundation in Computer Science, including programming languages, data structures, and software development, to successfully complete projects and contribute to team goals.","source_id":["EDU-1","SKILL-1","SKILL-6","SKILL-7","SKILL-8","SKILL-9"]},
               {"text":"Created a full-stack application using FastAPI, Supabase, React, and Groq, applying software engineering principles to develop a scalable and efficient solution.","source_id":["PROJ-P-1","PROJ-P-2","PROJ-P-3"]},
               {"text":"Demonstrated ability to work with modern languages and technologies, including Python, Groq, and SQL, with experience in developing and deploying software applications.","source_id":["SKILL-1","SKILL-2","SKILL-6","PROJ-RA-1","PROJ-OA-1"]}]

numbered_bullets = []
for i, bullet in enumerate(clean_bullets):
    numbered_bullets.append(f"Bullet {i}: {bullet['text']}")

bullets_text = "\n".join(numbered_bullets)





with open("profile.md","r") as f:
    content=f.read()

#print(content)

job_description="""As a Software Engineering Summer Scholar, you will get the opportunity to do full stack cloud native product development. You will be part of a cohort of software engineers, work in a 2-pizza scrum team model, developing highly scalable software with cutting edge technologies. You will use DevOps principles and practices to deliver code in CI/CD environments. You will get to work on complex problems for our clients while collaborating with team members from diverse backgrounds and experiences to build full stack cloud applications using the latest cloud technologies in a dynamic and agile environment. If you enjoyed your programming and data structure classes, you will get to apply all of those skills to solve real world challenges. You will also get to apply your engineering mindset to software product development across a diverse set of industries. We promise that you will never run out of challenges to learn and grow.

At Deloitte, we care about your success. With that in mind, you will get to progress on a technical career path that will allow you to grow into engineering roles, but with the ability to pivot across different parts of software development. You could choose to be a hands-on technical architect, a cloud integration expert, a DevOps expert, or any other technical role you want to pursue.

The Team

Our Deloitte Consulting team not only plays a major role in directly embedding technology insights into our clients’ organizational goals, but also designs, creates, implements, and deploys these solutions. Engagement teams at Deloitte drive value for our clients but also understand the importance of developing resources and contributing to the communities in which we work. We make it our business to create and deploy impactful solutions, both within and beyond a client setting.

 

Required Qualifications

Current enrollment in a full-time academic program with a target graduation date by Spring/Summer 2026
Bachelor's degree in progress in any STEM related discipline
Strong foundation with Computer Science (CS) subjects such as Software Engineering, Software Development, Programming Languages, Data Structures, Algorithms Design & Analysis, Operating Systems & System Programming, or Computer Architecture
Programming ability with at least one modern language like Java, C++, C#, Python as well as familiarity with object-oriented design
Must be legally authorized to work in the United States without the need for employer sponsorship, now or at any time in the future
Ability to travel up to 50%, on average, based on the work you do and the clients and industries/sectors you serve 
Must be at least 18 years of age at time of employment 
The wage range for this role takes into account the wide range of factors that are considered in making compensation decisions including but not limited to skill sets; experience and training; licensure and certifications; and other business and organizational needs. The disclosed range estimate has not been adjusted for the applicable geographic differential associated with the location at which the position may be filled. At Deloitte, it is not typical for an individual to be hired at or near the top of the range for their role and compensation decisions are dependent on the facts and circumstances of each case. A reasonable estimate is $41/hour. """



client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", 
        "content": f"""Here are tailored resume bullets for a job posting.
Job posting: {job_description}.
Bullets: {bullets_text}.
For each bullet, score it 0-100 based on how well it matches the
posting's language and priorities BY MEANING (not just literal word
overlap), its tone, and its length. Give brief feedback. Respond with
ONLY a JSON object with exactly this shape: {{"scores": [{{"index": 0,
"score": ..., "feedback": "..."}}]}}. No other text."""} 
    ],
  
    response_format={"type": "json_object"}
)
reply = completion.choices[0].message.content
data = json.loads(reply)
print(data)

final_bullets = []
for item in data['scores']:
    if item['score'] >= 70:
        final_bullets.append(clean_bullets[item['index']])

print("Final_bullets: ", final_bullets)