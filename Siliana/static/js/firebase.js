import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

// Firebase configuration (provided)
const firebaseConfig = {
  apiKey: "AIzaSyCsQtYPybdGlMt2v9cbjsqXXoMweb66dSs",
  authDomain: "pepiniere-9962d.firebaseapp.com",
  projectId: "pepiniere-9962d",
  storageBucket: "pepiniere-9962d.firebasestorage.app",
  messagingSenderId: "589369612402",
  appId: "1:589369612402:web:22ed872dd2db39558bcaeb",
  measurementId: "G-Q5C02LEKC1"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
