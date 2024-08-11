import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyC8Qv4xGxofjo8cfzK9R55GV2SIm8NrmUI",
  authDomain: "csie-nuk-692a6.firebaseapp.com",
  projectId: "csie-nuk-692a6",
  storageBucket: "csie-nuk-692a6.appspot.com",
  messagingSenderId: "470499671529",
  appId: "1:470499671529:web:4e0d9194d27d8aa455df78"
};


const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

export {
  storage
}