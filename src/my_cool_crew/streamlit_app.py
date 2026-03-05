import streamlit as st
import yaml
import os
from datetime import datetime
from my_cool_crew.crew import MyCoolCrew

AGENTS_PATH = os.path.join("config", "agents.yaml")
TASKS_PATH = os.path.join("config", "tasks.yaml")

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

st.set_page_config(layout="wide")
st.title("Настройка и запуск агентов")

agents_data = load_yaml(AGENTS_PATH)
tasks_data = load_yaml(TASKS_PATH)

col1, col2 = st.columns(2)

with col1:
    st.header("Агенты")
    for name, info in agents_data.items():
        with st.expander(f"Агент: {name}"):
            agents_data[name]['role'] = st.text_input("Role", value=info.get('role', ''), key=f"r_{name}")
            agents_data[name]['goal'] = st.text_area("Goal", value=info.get('goal', ''), key=f"g_{name}")
            agents_data[name]['backstory'] = st.text_area("Backstory", value=info.get('backstory', ''), key=f"b_{name}")

with col2:
    st.header("Задачи")
    for name, info in tasks_data.items():
        with st.expander(f"Задача: {name}"):
            tasks_data[name]['description'] = st.text_area("Description", value=info.get('description', ''), key=f"d_{name}")
            tasks_data[name]['expected_output'] = st.text_area("Expected Output", value=info.get('expected_output', ''), key=f"o_{name}")
            tasks_data[name]['agent'] = st.text_input("Assigned Agent", value=info.get('agent', ''), key=f"a_{name}")

st.divider()

topic = st.text_input("Тема (topic):", value="AI LLMs")

if st.button("Сохранить и запустить"):
    save_yaml(agents_data, AGENTS_PATH)
    save_yaml(tasks_data, TASKS_PATH)
    
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }
    
    st.write("Выполнение...")
    result = MyCoolCrew().crew().kickoff(inputs=inputs)
    
    st.subheader("Результат:")
    st.markdown(result.raw)