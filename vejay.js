import { initializeApp } from "firebase/app";
import { getDatabase, ref, set } from "firebase/database";

const firebaseConfig = {
    apiKey: "AIzaSyDTV8Ga-maKTuJQhmL1wZPCX_fqdnYT83U",
    authDomain: "contactform-a2722.firebaseapp.com",
    databaseURL: "https://contactform-a2722-default-rtdb.firebaseio.com",
    projectId: "contactform-a2722",
    storageBucket: "contactform-a2722.appspot.com",
    messagingSenderId: "938144955245",
    appId: "1:938144955245:web:a62c5c6cf604fb25d6f864"
  };
  
  // initialize firebase
  const app=initializeApp(firebaseConfig);
  var contactFormDB = firebase.database().ref("sandy",);
  var newContactForm = contactFormDB.push();
  
 sub.addEventListener('click',(e)=>{
    var name = document.getElementById('name').value;
    var emailid = document.getElementById('emailid').value;
    
    writeUserData("1", name,emailid);})

  function writeUserData(userId, name, emailid) {
    const db = getDatabase();
    const reference = ref(db, 'users/'+userId);
    reference.set( {
      username: name,
      email: emailid,
      
  });
   }
  