import streamlit as st
from streamlit_drawable_canvas import st_canvas


# Streamlit 
st.set_page_config(page_title='Reconocimiento de Dígitos escritos a mano', layout='wide')
st.title('Reconocimiento de Dígitos escritos a mano')
st.subheader("Dibuja el digito en el panel  y presiona  'Predecir'")

# Add canvas component
# Specify canvas parameters in application
drawing_mode = "freedraw"
stroke_width = st.slider('Selecciona el ancho de línea', 1, 30, 15)
stroke_color = '#FFFFFF' # Set background color to white
bg_color = '#000000'

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=1200,
    width=1200,
    key="canvas",
)

ke = st.text_input('Ingresa tu Clave')
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = ke


# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

analyze_button = st.button("Analiza la imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')
        
      # Codificar la imagen en base64
 
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = (f"Describe in spanish briefly the image")
    
      # Create the payload for the completion request
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url":f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]
    
        # Make the request to the OpenAI API
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model= "gpt-4o-mini",  #o1-preview ,gpt-4o-mini
              messages=[
                {
                   "role": "user",
                   "content": [
                     {"type": "text", "text": prompt_text},
                     {
                       "type": "image_url",
                       "image_url": {
                         "url": f"data:image/png;base64,{base64_image}",
                       },
                     },
                   ],
                  }
                ],
              max_tokens=500,
              )
            #response.choices[0].message.content
            if response.choices[0].message.content is not None:
                    full_response += response.choices[0].message.content
                    message_placeholder.markdown(full_response + "▌")
            # Final update to placeholder after the stream ends
            message_placeholder.markdown(full_response)
            if Expert== profile_imgenh:
               st.session_state.mi_respuesta= response.choices[0].message.content #full_response 
    
            # Display the response in the app
            #st.write(response.choices[0])
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    # Warnings for user action required

    if not api_key:
        st.warning("Por favor ingresa tu API key.")
