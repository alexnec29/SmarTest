import streamlit as st
import sys
import os

# Adăugăm folderul rădăcină la calea Python pentru a putea importa modulele din 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.test_builder import TestBuilder
from core.evaluator import evaluate_answer, load_keywords_for_topic

# Configurare pagină
st.set_page_config(page_title="SmarTest AI", page_icon="🎓", layout="wide")


def main():
    st.title("🎓 SmarTest - Generator de Teste AI")
    st.markdown("Această aplicație generează întrebări de examen și îți evaluează automat răspunsurile.")

    # --- Initializare Builder ---
    builder = TestBuilder()

    # --- SIDEBAR: Configurare ---
    st.sidebar.header("🛠️ Configurare Test")

    # 1. Selectare Subiecte
    topics_map = builder.get_available_topics()
    selected_topic_names = st.sidebar.multiselect(
        "Selectează Capitolele:",
        options=list(topics_map.values()),
        default=list(topics_map.values())  # Implicit toate selectate
    )

    # Convertim numele înapoi în ID-uri pentru backend
    selected_topic_ids = [tid for tid, name in topics_map.items() if name in selected_topic_names]

    # 2. Selectare Număr Întrebări
    num_questions = st.sidebar.number_input("Număr de întrebări:", min_value=1, max_value=20, value=3)

    # 3. Buton Generare
    if st.sidebar.button("🚀 Generează Test Nou", type="primary"):
        if not selected_topic_ids:
            st.sidebar.error("Selectează cel puțin un capitol!")
        else:
            with st.spinner("🤖 Asistentul AI generează întrebările..."):
                try:
                    # Generăm întrebările folosind logica ta existentă
                    questions, answers = builder.generate_test(selected_topic_ids, num_questions)

                    # Salvăm în starea sesiunii (pentru a nu le pierde la refresh)
                    st.session_state['questions'] = questions
                    st.session_state['correct_answers'] = answers
                    st.session_state['user_answers'] = [""] * len(questions)
                    st.session_state['scores'] = [None] * len(questions)  # None = neevaluat
                    st.success("Test generat cu succes!")
                except Exception as e:
                    st.error(f"Eroare la generare: {e}")

    # --- ZONA PRINCIPALĂ: Afișare Întrebări ---
    if 'questions' in st.session_state and st.session_state['questions']:
        st.divider()

        for i, q in enumerate(st.session_state['questions']):
            # Container pentru fiecare întrebare
            with st.container():
                st.subheader(f"Întrebarea {i + 1}")
                st.caption(f"Topic: {q['topic_name']}")

                # Afișare text întrebare
                st.info(q['question'])

                # Câmp input răspuns
                user_ans = st.text_area(
                    f"Răspunsul tău:",
                    key=f"ans_{i}",
                    height=100,
                    placeholder="Scrie rezolvarea aici..."
                )

                # Buton Verificare Individuală
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button(f"Verifică Răspunsul {i + 1}", key=f"btn_{i}"):
                        if not user_ans.strip():
                            st.warning("Te rugăm să scrii un răspuns înainte de verificare.")
                        else:
                            # 1. Încărcăm răspunsul corect
                            correct_ans = st.session_state['correct_answers'][i]

                            # 2. Încărcăm keywords pentru topicul respectiv
                            keywords = load_keywords_for_topic(q['topic'])

                            # 3. Evaluăm folosind funcția ta îmbunătățită
                            score = evaluate_answer(correct_ans, user_ans, keywords)

                            # Salvăm scorul
                            st.session_state['scores'][i] = score

                # Afișare Rezultat Evaluare
                if st.session_state['scores'][i] is not None:
                    score = st.session_state['scores'][i]
                    correct_ans = st.session_state['correct_answers'][i]

                    with col2:
                        if score == 100:
                            st.success(f"**Scor: {score}%** - Excelent! 🎉")
                        elif score >= 50:
                            st.warning(f"**Scor: {score}%** - Destul de bine.")
                        else:
                            st.error(f"**Scor: {score}%** - Răspuns incorect sau incomplet.")

                        # Afișare răspuns corect într-un meniu expandabil (spoiler)
                        with st.expander("Vezi răspunsul corect"):
                            st.markdown(f"**Răspunsul așteptat:**\n\n{correct_ans}")

            st.divider()

    else:
        # Mesaj de întâmpinare când nu e generat testul
        st.info("👈 Folosește meniul din stânga pentru a configura și genera un test nou.")


if __name__ == "__main__":
    main()