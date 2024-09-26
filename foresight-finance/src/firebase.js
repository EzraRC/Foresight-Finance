// Import the functions you need from the Firebase SDKs
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore"; // Import Firestore

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAv_CECwXyUUUs6dIOiU3qsePQBeJZBjMs",
  authDomain: "foresight-finance.firebaseapp.com",
  projectId: "foresight-finance",
  storageBucket: "foresight-finance.appspot.com",
  messagingSenderId: "283263851996",
  appId: "1:283263851996:web:9b9c02fc1875117524c319",
  measurementId: "G-VW6875BH0K"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Analytics (Optional)
const analytics = getAnalytics(app);

// Initialize Firebase Authentication
const auth = getAuth(app);

// Initialize Firestore
const db = getFirestore(app); // Correct Firestore initialization

// Export the necessary Firebase services
export { auth, db, app, analytics };
