from search_vector.task_05 import search
import streamlit as st


st.markdown("""
<style>
.big-font {
    text-align: center;
    font-size:60px !important;
    color:#000000;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Find Your Song!</p>', unsafe_allow_html=True)
query = st.text_input("Search:")

if query:
    try:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(' ')

        with col2:
            st.subheader("Results:")
            results = search(query)
            if results:
                for result in results:
                    st.markdown(
                        f"**№** {result['doc_id']} | **Link:** [{result['link']}]"
                        f"({result['link']}) | **Similarity:** {result['cosine_sim']:.2f}")
            else:
                st.write("No results found.")
        with col3:
            st.write(' ')

    except KeyError:
        pass
