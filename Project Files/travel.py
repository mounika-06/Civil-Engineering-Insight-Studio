
import streamlit as st
import google.generativeai as genai

# Configure API key
api_key = "AIzaSyDdtGua6zuEoXaEhYpLDzF3yg3ZyFSao10"
genai.configure(api_key=api_key)

# Function to generate a travel itinerary based on user input
def generate_itinerary(destination, days, nights):
    # Create the model configuration
    generation_config = {
        "temperature": 0.4,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the Generative Model (MODE CHANGED)
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        generation_config=generation_config,
    )

    # Start a new chat session with the model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"write me a travel itinerary to {destination} for {days} days and {nights} nights",
                ],
            },
        ]
    )

    # Send a message to the chat session and get the response
    response = chat_session.send_message(
        f"Create a detailed travel itinerary for {days} days and {nights} nights in {destination}."
    )

    # Return the generated itinerary
    return response.text


def main():
    # Streamlit app
    st.title("Travel Itinerary Generator")

    # Get user inputs
    destination = st.text_input("Enter your desired destination:")
    days = st.number_input("Enter the number of days:", min_value=1)
    nights = st.number_input("Enter the number of nights:", min_value=0)

    # Ensure that user inputs are provided
    if st.button("Generate Itinerary"):
        if destination.strip() and days > 0 and nights >= 0:
            try:
                itinerary = generate_itinerary(destination, days, nights)
                st.text_area("Generated Itinerary:", value=itinerary, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please make sure all inputs are provided and valid.")


if __name__ == "__main__":
    main()