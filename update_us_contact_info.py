import os

# Update Executive Resume
resume_path = r'C:\Users\dkven\.gemini\antigravity\brain\df9e8416-acff-4abf-943f-408e96928da4\Diego_Kasper_Romero_Diaz_Executive_Resume.md'
with open(resume_path, 'r', encoding='utf-8') as f:
    res_code = f.read()

res_code = res_code.replace(
    "Porto Alegre, Brazil | Remote / Global (90% Travel Ready) | US B1/B2 Visa Active",
    "1696 Carrington Pointe, Tucker, GA 30084, USA | Porto Alegre, Brazil | Remote / Global (90% Travel Ready)"
)

res_code = res_code.replace(
    "Email: kasper@dktimber.com | Phone: +55 51 99107-4142 | US Line: +1 (470) 406-7080",
    "US Address: 1696 Carrington Pointe, Tucker, GA 30084 | US Mobile: +1 (470) 406-7080 | BR Mobile: +55 51 99107-4142 | Email: kasper@dktimber.com"
)

with open(resume_path, 'w', encoding='utf-8') as f:
    f.write(res_code)

print("Updated Diego_Kasper_Romero_Diaz_Executive_Resume.md with US address and mobile numbers!")

# Update Placement Plan
plan_path = r'C:\Users\dkven\.gemini\antigravity\brain\df9e8416-acff-4abf-943f-408e96928da4\Diego_Timber_Industry_Placement_Plan.md'
with open(plan_path, 'r', encoding='utf-8') as f:
    plan_code = f.read()

plan_code = plan_code.replace(
    "kasper@dktimber.com | +55 51 99107-4142 | +1 (470) 406-7080\nPorto Alegre, Brazil (Remote / Global)",
    "1696 Carrington Pointe, Tucker, GA 30084, USA\nUS: +1 (470) 406-7080 | BR: +55 51 99107-4142 | Email: kasper@dktimber.com"
)

with open(plan_path, 'w', encoding='utf-8') as f:
    f.write(plan_code)

print("Updated Diego_Timber_Industry_Placement_Plan.md with US address and mobile numbers!")
