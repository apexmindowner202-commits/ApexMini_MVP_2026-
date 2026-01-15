streamlit
requests
// ==========================================

// APEXMINI_CORE: STERIL, BERBOBOT, UNLIMITED

// ==========================================



import { OpenRouter } from '@openrouter/sdk';



// 1. RUH OTAK (DISKUSI & JAWABAN MURNI)

const openRouter = new OpenRouter({

  apiKey: '<OPENROUTER_API_KEY>' // Suntikkan API Key 

});



async function processPrompt(userPrompt) {

  const response = await openRouter.chat.send({

    model: 'openai/gpt-5.2', // Target Otak Internasional

    messages: [{ role: 'user', content: userPrompt }],

  });

  return response.choices[0].message; // BALASAN MURNI

}



// 2. PIPA UPLOAD RAKSASA (TANPA BATAS MAKSIMAL)

const uploadBtn = document.getElementById('upload-btn');

uploadBtn.onclick = () => {

  const input = document.createElement('input');

  input.type = 'file';

  input.multiple = true; // KUNCI: GILAS SEMUANYA!

  

  input.onchange = async (e) => {

    const files = Array.from(e.target.files);

    console.log(LOG: Memproses ${files.length} File Visual...);

    

    for (const file of files) {

      try {

        await execute_visual_model(file); // MODEL VISUAL OPEN SOURCE

        console.log("STATUS: FILE_SUKSES_DIGILAS");

      } catch (err) {

        console.log("RETRY: ULANGI EKSEKUSI...");

      }

    }

  };

  input.click();

};



// 3. LOGIKA EKSEKUSI TOMBOL SEND

document.getElementById('send-btn').onclick = async () => {

  const prompt = document.getElementById('user-prompt').value;

  const reply = await processPrompt(prompt);

  document.getElementById('chat-box').innerHTML += <p>${reply}</p>;

};





  

    

<div id="chat-box"></div>

<div class="input-area">
    <button id="upload-btn">+</button> <input type="text" id="user-prompt" placeholder=""> <button id="send-btn">Send</button>
</div>



