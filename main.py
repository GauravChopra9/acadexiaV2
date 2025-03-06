import streamlit as st
import asyncio
from api import fetch_clips, fetch_slides
import time

async def main():
    # Initialize session state
    if 'init' not in st.session_state:
        st.session_state.init = True
        st.session_state.clips_query = None
        st.session_state.clips = None
        st.session_state.slides_query = None
        st.session_state.ppts = None
        st.session_state.ppt_titles = None
        st.session_state.page_nums_list = None
        st.session_state.ppt_explanations_list = None
        st.session_state.current_pages = {}  # Track current page for each presentation
        st.session_state.pdf_key = 0  # Use this to force PDF rerender

    tab1, tab2 = st.tabs(["Lecture Clip Search 📹", "PowerPoint Search 🎒"])

    tab1.subheader("Econ 301 Lecture Clip Search")
    tab2.subheader("Econ 301 PowerPoint Search")

    # Tab 1 remains the same...
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
                for idx, clip in enumerate(clips):
                    with st.expander(f"{clip['start_time']} - {clip['end_time']}"):
                        st.markdown(
                            f"""
                            <div style="text-align: center;">
                                {clip['embed_link']}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        st.divider()
                        st.subheader('Explanation')
                        st.write(clip['explanation'])
            else:
                st.warning("No clips found for your query.")

    with tab2:
        slides_search_bar = st.text_input("Find me slides about...")

        # Handle new search query
        # if slides_search_bar and slides_search_bar != st.session_state.slides_query:
        #     st.session_state.slides_query = slides_search_bar
        #     with st.spinner("Searching for slides..."):
        #         try:
        #             response = await fetch_slides(slides_search_bar)
        #             st.session_state.ppts, st.session_state.ppt_titles, st.session_state.page_nums_list, st.session_state.ppt_explanations_list = response
        #             # Initialize current pages for new search
        #             st.session_state.current_pages = {
        #                 idx: st.session_state.page_nums_list[idx][0]
        #                 for idx in range(len(st.session_state.ppts))
        #             }
        #         except Exception as e:
        #             st.error(f"An error occurred: {e}")
        #             return

        # if st.session_state.ppts:
        #     st.success(f"Found {len(st.session_state.ppts)} presentations!")
            
        #     for idx, (ppt, title) in enumerate(zip(st.session_state.ppts, st.session_state.ppt_titles)):
        #         with st.expander(title):
        #             if ppt:
        #                 col1, col2 = st.columns([2, 1])
                        
        #                 with col1:
        #                     current_page = st.session_state.current_pages[idx]
                            
        #                     # Create a unique container for each PDF
        #                     pdf_container = st.empty()
                            
        #                     try:
        #                         pdf_container.markdown(
        #                             f"""
        #                             <div style="width: 100%; height: 800px; overflow: hidden;">
        #                                 <iframe 
        #                                     src="data:application/pdf;base64,{ppt}#page={current_page}"
        #                                     width="100%" 
        #                                     height="100%" 
        #                                     style="border: none;"
        #                                     allow="fullscreen"
        #                                 ></iframe>
        #                             </div>
        #                             """,
        #                             unsafe_allow_html=True
        #                         )
        #                     except Exception as e:
        #                         st.error(f"Error rendering PDF: {e}")
                        
        #                 with col2:
        #                     st.write("### Navigation")
                            
        #                     # Get page information
        #                     pages = st.session_state.page_nums_list[idx]
        #                     explanations = st.session_state.ppt_explanations_list[idx]
        #                     current_index = pages.index(current_page)
                            
        #                     # Navigation controls
        #                     cols = st.columns(3)
                            
        #                     # Previous button
        #                     if cols[0].button("← Prev", key=f"prev_{idx}", 
        #                                     disabled=current_index == 0):
        #                         st.session_state.current_pages[idx] = pages[current_index - 1]
        #                         st.session_state.pdf_key += 1
        #                         st.rerun()
                            
        #                     # Page selector
        #                     selected_page = cols[1].selectbox(
        #                         "Page",
        #                         pages,
        #                         index=current_index,
        #                         key=f"page_select_{idx}"
        #                     )
                            
        #                     if selected_page != current_page:
        #                         st.session_state.current_pages[idx] = selected_page
        #                         st.session_state.pdf_key += 1
        #                         st.rerun()
                            
        #                     # Next button
        #                     if cols[2].button("Next →", key=f"next_{idx}", 
        #                                     disabled=current_index == len(pages) - 1):
        #                         st.session_state.current_pages[idx] = pages[current_index + 1]
        #                         st.session_state.pdf_key += 1
        #                         st.rerun()
                            
        #                     st.write("### Explanation")
        #                     st.write(explanations[current_index])

if __name__ == "__main__":
    asyncio.run(main())
