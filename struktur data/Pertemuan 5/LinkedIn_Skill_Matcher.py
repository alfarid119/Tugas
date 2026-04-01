import streamlit as st

# 1. Dictionary job_requirements
job_requirements = {
    "Data Scientist": ["Python", "Math", "AI"],
    "Web Developer": ["JavaScript", "HTML", "CSS"],
    "UI/UX Designer": ["Figma", "Creativity", "Communication"],
    "Cybersecurity Analyst": ["Networking", "Python", "Risk Management"]
}

# 2. Tampilan judul
st.title("LinkedIn Skill Matcher")

# 3. Tampilkan keterangan skill yang dibutuhkan
st.write("### Skill yang Dibutuhkan untuk Setiap Pekerjaan")
for job, skills in job_requirements.items():
    st.write(f"**{job}**: {', '.join(skills)}")

# 4. Input skill user
user_input = st.text_input("Masukkan skill Anda (pisahkan dengan koma):")
user_skills = [skill.strip() for skill in user_input.split(",") if skill]

# 5. Hitung persentase kecocokan
results = {}
if user_skills:
    for job, skills in job_requirements.items():
        match_count = len(set(user_skills) & set(skills))
        match_percentage = (match_count / len(skills)) * 100
        results[job] = match_percentage

    # 6. Output dengan progress bar
    st.write("### Hasil Kecocokan Skill")
    for job, score in results.items():
        st.write(f"{job}: {score:.2f}%")
        st.progress(int(score))
