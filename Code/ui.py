import streamlit as st
from text_generator_llama3 import generate_story
from moderation import is_prompt_appropriate
from utils import combine_inputs, generate_prompt

#page config
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="🖋️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

#styling
st.markdown(
    """
    <style>
    body {
        background-color: #525252;
        color: #333;
        font-family: Arial, sans-serif;
    }
    hr {
        border: none;
        border-top: 2px solid #FF4040;
    }
    h3 {
        color: #FF4040;
        margin-bottom: 15px;
    }
    .stButton > button {
        background-color: #FF4040;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 8px 20px;
    }
    .stButton > button:hover {
        background-color: #3d3d3d; /* Dark grey on hover */ 
        color: white !important;
    }
    .stButton > button:active {
        background-color: #525252; /* Same as page background */
        color: white !important;
        box-shadow: none; /* Remove default shadow */
    }
    .how-to-box {
        background-color: #3d3d3d;
        border: 2px solid #FF4040;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


#title and instructions
st.title("🖋️ AI Story Generator")
st.markdown("**Designed by Adin Vella. Powered by Llama3.2-3B.**")
st.markdown(
    """
    <div class="how-to-box">
        <h3>📖 How to Use</h3>
        <p>
            1. Enter the main idea for your story in the "Main Story Idea" section.<br>
            2. Choose or add custom options for the genre, theme, tone, key character role, and setting.<br>
            3. Adjust the creativity level (higher values produce more imaginative results).<br>
            4. Click "Generate Story" to create your story.<br>
            5. Refine your story by providing feedback and applying changes.<br>
            6. Save your story to a file once you're satisfied.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

#separator style
def section_separator(title):
    st.markdown(f"""
    <hr>
    <h3>{title}</h3>
    """, unsafe_allow_html=True)

#user input
section_separator("Main Story Idea")
main_idea = st.text_input(
    "Enter the main idea of the story (one sentence only):",
    value="",
    help="Provide a concise idea to guide the story generation.",
)

section_separator("Genre Selection")
genre_options = ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Horror", "Romance", "Comedy", "Drama"]
custom_genre = st.text_input("Add a custom genre (optional):", key="custom_genre")
if custom_genre and custom_genre not in genre_options:
    genre_options.append(custom_genre)
genre = st.selectbox("Choose a genre:", genre_options, index=genre_options.index(custom_genre) if custom_genre else 0)
st.markdown(f"**Selected Genre:** {genre}")

section_separator("Theme Selection")
theme_options = ["Adventure", "Revenge", "Love", "Betrayal", "Redemption", "Discovery", "Courage", "Friendship", "Survival"]
custom_theme = st.text_input("Add a custom theme (optional):", key="custom_theme")
if custom_theme and custom_theme not in theme_options:
    theme_options.append(custom_theme)
theme = st.selectbox("Choose a theme:", theme_options, index=theme_options.index(custom_theme) if custom_theme else 0)
st.markdown(f"**Selected Theme:** {theme}")

section_separator("Tone Selection")
tone_options = ["Humorous", "Serious", "Suspenseful", "Dramatic", "Dark", "Whimsical", "Optimistic"]
custom_tone = st.text_input("Add a custom tone (optional):", key="custom_tone")
if custom_tone and custom_tone not in tone_options:
    tone_options.append(custom_tone)
tone = st.selectbox("Choose a tone:", tone_options, index=tone_options.index(custom_tone) if custom_tone else 0)
st.markdown(f"**Selected Tone:** {tone}")

section_separator("Key Character Role")
key_character_options = ["Protagonist", "Hero", "Villain", "Sidekick", "Antihero"]
custom_key_character = st.text_input("Add a custom character role (optional):", key="custom_key_character")
if custom_key_character and custom_key_character not in key_character_options:
    key_character_options.append(custom_key_character)
key_character = st.selectbox("Choose a key character role:", key_character_options, index=key_character_options.index(custom_key_character) if custom_key_character else 0)
st.markdown(f"**Selected Key Character Role:** {key_character}")

section_separator("Setting Selection")
setting_options = ["Magical Forest", "Futuristic City", "Haunted Castle", "Space Station", "Medieval Kingdom", "Desert Oasis", "Underground Cavern"]
custom_setting = st.text_input("Add a custom setting (optional):", key="custom_setting")
if custom_setting and custom_setting not in setting_options:
    setting_options.append(custom_setting)
setting = st.selectbox("Choose a setting:", setting_options, index=setting_options.index(custom_setting) if custom_setting else 0)
st.markdown(f"**Selected Setting:** {setting}")

section_separator("Creativity Level")
temperature = st.slider("Adjust creativity level:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)

input_combined = combine_inputs(main_idea, genre, theme, tone, key_character, setting)
prompt = generate_prompt(main_idea, genre, theme, tone, key_character, setting)

#init session states
if "story_versions" not in st.session_state:
    st.session_state.story_versions = []
if "current_story" not in st.session_state:
    st.session_state.current_story = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "refined" not in st.session_state:
    st.session_state.refined = False

#for story gen
section_separator("Generate Your Story")
if st.button("Generate Story"):
    moderation_status = st.empty()

    with st.spinner("Moderating input content..."):
        is_appropriate, flagged_categories = is_prompt_appropriate(input_combined)

    if is_appropriate:
        moderation_status.success("Prompt input moderation - Done ✅")

        with st.spinner("Generating your story..."):
            try:
                generated_story = generate_story(prompt, temperature=temperature)
                st.session_state.current_story = generated_story
                st.session_state.story_versions.append(generated_story)
                st.subheader("Generated Story")
                st.text_area("Your Story:", value=st.session_state.current_story, height=300)
            except Exception as e:
                st.error(f"Error generating story: {e}")
    else:
        st.error("Your input contains inappropriate content.")
        st.markdown("### 🚩 Flagged Issues:")
        if flagged_categories:
            for category, score in flagged_categories:
                st.markdown(f"- **{category.capitalize()}**: {score:.2f}")

#refinement loop
if st.session_state.current_story:
    section_separator("Refine Your Story")
    st.text_area(
        "Provide instruction/s for refinement:",
        value=st.session_state.feedback,
        height=100,
        key="feedback_area",
        on_change=lambda: st.session_state.update({"feedback": st.session_state["feedback_area"]}),
    )

    if st.button("Apply Changes"):
        #moderation tal feedback
        with st.spinner("Moderating refinement instructions..."):
            is_appropriate, flagged_categories = is_prompt_appropriate(st.session_state.feedback)

        if is_appropriate:
            with st.spinner("Applying changes..."):
                try:
                    refine_prompt = (
                        f"Refine/Update this story:\n{st.session_state.current_story}\n\n"
                        f"With these instructions:\n{st.session_state.feedback}\n\n"
                        "Ensure the changes are coherent."
                        "As your output, provide only the updated story."
                    )
                    updated_story = generate_story(refine_prompt, temperature=temperature)
                    st.session_state.current_story = updated_story
                    st.text_area("Updated Story:", value=st.session_state.current_story, height=300)
                    st.session_state.refined = True
                except Exception as e:
                    st.error(f"Error applying changes: {e}")
        else:
            st.error("Your refinement instructions contain inappropriate content.")
            st.markdown("### 🚩 Flagged Issues:")
            if flagged_categories:
                for category, score in flagged_categories:
                    st.markdown(f"- **{category.capitalize()}**: {score:.2f}")

    #showing accept/reject options post-refinement
    if st.session_state.refined:
        section_separator("Accept or Reject Changes")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Accept Changes"):
                st.session_state.story_versions.append(st.session_state.current_story)
                st.success("Changes accepted. Current version has been added to the review section.")
                st.session_state.refined = False

        with col2:
            #revert back to prev if rejected
            if st.button("Reject Changes"):
                st.info("Changes rejected. Reverting to the previous version.")
                if len(st.session_state.story_versions) > 0:
                    st.session_state.current_story = st.session_state.story_versions[-1]
                else:
                    st.warning("No previous version to revert to.")
                st.session_state.refined = False

#story versions
section_separator("Review Story Versions")
if st.session_state.story_versions:
    for idx, version in enumerate(st.session_state.story_versions):
        st.markdown(f"**Version {idx + 1}:**")
        st.text_area(f" ", value=version, height=200, key=f"version_{idx}")

