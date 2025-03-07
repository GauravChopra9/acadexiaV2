import streamlit as st
import asyncio
from api import fetch_clips

async def main():
    tab1, tab2 = st.tabs(["Lecture Clip Search 🎥", "PowerPoint Search 🎒"])

    tab1.subheader("Econ 301 Lecture Clip Search")
    tab2.subheader("Econ 301 PowerPoint Search")

    session_defaults = {
        'clips_query': None, 'clips': None, 'slides_query': None, 'ppts': None,
        'ppt_titles': None, 'page_nums_list': None, 'ppt_explanations_list': None,
        'current_page': {}, 'current_explanation': {}, 'open_expander': None,
        'page_selection': {}
    }
    
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

    with tab1:
        clips_search_bar = st.text_input("Find me clips about...")

        if clips_search_bar and clips_search_bar != st.session_state.clips_query:
            st.session_state.clips_query = clips_search_bar
            st.session_state.clips = None

        if st.session_state.clips_query:
            if st.session_state.clips is None:
                with st.spinner("Searching for clips..."):
                    try:
                        st.session_state.clips = await fetch_clips(st.session_state.clips_query)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.session_state.clips = []

            clips = st.session_state.clips
            if clips:
                st.success(f"Found {len(clips)} clips!")
                for clip in clips:
                    with st.expander(f"{clip['start_time']} - {clip['end_time']}"):
                        st.markdown(f"""
                            <div style="text-align: center;">
                                {clip['embed_link']}
                            </div>
                        """, unsafe_allow_html=True)
                        st.divider()
                        st.subheader('Explanation')
                        st.write(clip['explanation'])
            else:
                st.warning("No clips found for your query.")

    with tab2:
        slides_search_bar = st.text_input("Find me slides about...")

        # if slides_search_bar and slides_search_bar != st.session_state.slides_query:
        #     st.session_state.slides_query = slides_search_bar
        #     st.session_state.current_page.clear()
        #     st.session_state.current_explanation.clear()

        #     with st.spinner("Searching for slides..."):
        #         try:
        #             response = await fetch_slides(st.session_state.slides_query)
        #             (st.session_state.ppts, st.session_state.ppt_titles, 
        #              st.session_state.page_nums_list, st.session_state.ppt_explanations_list) = response
        #         except Exception as e:
        #             st.error(f"An error occurred: {e}")
        
        # def handle_page_change(idx):
        #     if st.session_state.page_selection.get(idx) is not None:
        #         page_idx = st.session_state.page_nums_list[idx].index(st.session_state.page_selection[idx])
        #         st.session_state.current_page[idx] = st.session_state.page_selection[idx]
        #         st.session_state.current_explanation[idx] = st.session_state.ppt_explanations_list[idx][page_idx]
        #         st.session_state.open_expander = idx

        
        # if st.session_state.ppts:
        #     st.success(f"Found {len(st.session_state.ppts)} slides!")
        #     for idx, ppt in enumerate(st.session_state.ppts):
        #         is_open = st.session_state.open_expander == idx
        #         with st.expander(st.session_state.ppt_titles[idx], expanded=is_open):
        #             # Show the explanation
        #             if idx not in st.session_state.current_explanation:
        #                 st.session_state.current_explanation[idx] = st.session_state.ppt_explanations_list[idx][0]

        #             st.write(st.session_state.current_explanation[idx])
        #             st.divider()

        #             # Initialize the selected page number
        #             if idx not in st.session_state.current_page:
        #                 st.session_state.current_page[idx] = st.session_state.page_nums_list[idx][0]

        #             # Callback function to update the displayed page and explanation
        #             def handle_page_change(new_page, idx=idx):
        #                 st.session_state.current_page[idx] = new_page
        #                 page_idx = st.session_state.page_nums_list[idx].index(new_page)
        #                 st.session_state.current_explanation[idx] = st.session_state.ppt_explanations_list[idx][page_idx]
        #                 st.session_state.open_expander = idx

        #             # Slide navigation using radio buttons
        #             st.write("More Slides")
        #             selected_page = st.radio(
        #                 label="Select a slide:",
        #                 options=st.session_state.page_nums_list[idx],
        #                 index=st.session_state.page_nums_list[idx].index(st.session_state.current_page[idx]),
        #                 key=f"radio_{idx}_{st.session_state.slides_query}",
        #                 horizontal=True
        #             )

        #             # Ensure the radio button selection updates the PDF display
        #             if selected_page != st.session_state.current_page[idx]:
        #                 handle_page_change(selected_page, idx)

        #             st.write("")  # Add space after buttons

        #             # Convert selected page to match PDF page indexing
        #             page_to_show = max(1, int((st.session_state.current_page[idx] + 1) / 2))

        #             # Embed PDF with the selected page
        #             pdf_display = f"""
        #                 <embed src="data:application/pdf;base64,{ppt}#page={page_to_show}" 
        #                     width="650" height="900" type="application/pdf">
        #             """
        #             st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    asyncio.run(main())
