import streamlit as st
import sys
import os
from datetime import datetime

# Добавляем путь к папке src, чтобы Python видел ваш crew
sys.path.append(os.path.join(os.getcwd(), "src"))

# Теперь импорт должен заработать (проверьте, что папка в src называется именно так)
try:
    from my_cool_crew.crew import MyCoolCrew
except ImportError:
    st.error("Не удалось найти модуль MyCoolCrew. Проверьте название папки в src/")
    st.stop()

st.set_page_config(page_title="CrewAI AI")

st.title("🚀 Мультиагентная система управления")

# Боковая панель с настройками
with st.sidebar:
    st.header("Настройки")
    topic = st.text_input("Тема исследования:", value="AI LLMs")
    run_button = st.button("Запустить экипаж", type="primary")

# Основная область
if run_button:
    with st.status("🤖 Агенты работают...", expanded=True) as status:
        st.write("Инициализация экипажа...")
        
        inputs = {
            'topic': topic,
            'current_year': str(datetime.now().year)
        }
        
        try:
            # Запуск логики CrewAI
            result = MyCoolCrew().crew().kickoff(inputs=inputs)
            
            status.update(label="✅ Готово!", state="complete", expanded=False)
            
            st.subheader("Результат работы:")
            st.markdown(result.raw)
            
            # Если есть файл, даем скачать
            if hasattr(result, 'tasks_output'):
                st.download_button(
                    label="Скачать отчет (.md)",
                    data=result.raw,
                    file_name="report.md",
                    mime="text/markdown"
                )
                
        except Exception as e:
            st.error(f"Ошибка: {e}")
            status.update(label="❌ Ошибка выполнения", state="error")
else:
    st.info("Введите тему и нажмите кнопку запуска для начала работы агентов.")