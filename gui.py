
import streamlit as st
from book_view import BookManager

book_instance = BookManager()

tab1, tab2, tab3, tab4 = st.tabs(
    ["ADD", "VIEW", "UPDATE", "DELETE"]
)


# ADD BOOK
with tab1:
    st.header("Add New Book")

    book_name = st.text_input("Enter Book Name")
    author_name = st.text_input("Enter Author Name")
    price = st.number_input("Enter Price", min_value=0.0)
    typee = st.text_input("Enter Genre")
    published_year = st.number_input(
        "Year of Publish", min_value=0, step=1
    )

    if st.button("Add New Book"):
        if book_name and author_name and typee:
            book_instance.post(
                book_name=book_name,
                author_name=author_name,
                price=price,
                typee=typee,
                published_year=published_year
            )

            st.success("New book added successfully!")
        else:
            st.warning("Please fill all fields")


# VIEW BOOKS
with tab2:
    st.header("View All Books")

    records = book_instance.retrieve()

    if records:
        st.table(records)
    else:
        st.warning("No book details found")


# UPDATE BOOK
with tab3:
    st.header("Update Book Details")

    book_id = st.number_input(
        "Enter Book ID",
        min_value=1,
        step=1,
        key="update_id"
    )

    if st.button("Get Book Details"):
        record = book_instance.get_object(book_id)

        if record:
            st.session_state["selected_book"] = record
        else:
            st.session_state.pop("selected_book", None)
            st.error("Book not found")

    if "selected_book" in st.session_state:

        record = st.session_state["selected_book"]

        st.subheader("Edit Book")

        # Assumes record order:
        # id, book_name, author_name, price, typee, published_year

        new_book_name = st.text_input(
            "Book Name", value=record[1]
        )

        new_author_name = st.text_input(
            "Author Name", value=record[2]
        )

        new_price = st.number_input(
            "Price", min_value=0.0,
            value=float(record[3])
        )

        new_typee = st.text_input(
            "Genre", value=record[4]
        )

        new_published_year = st.number_input(
            "Published Year",
            min_value=0,
            value=int(record[5]),
            step=1
        )

        if st.button("Update Book"):
            book_instance.put(
                book_id,
                book_name=new_book_name,
                author_name=new_author_name,
                price=new_price,
                typee=new_typee,
                published_year=new_published_year
            )

            st.success("Book updated successfully!")
            del st.session_state["selected_book"]
            st.rerun()


# DELETE BOOK
with tab4:
    st.header("Delete Book")

    delete_id = st.number_input(
        "Enter Book ID to Delete",
        min_value=1,
        step=1,
        key="delete_id"
    )

    if st.button("Delete Book"):
        record = book_instance.get_object(delete_id)

        if record:
            book_instance.delete(delete_id)
            st.success("Book deleted successfully!")
        else:
            st.error("Book not found")


book_instance.connection.close()
