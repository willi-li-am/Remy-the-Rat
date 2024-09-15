import './App.css';
import { remyBase64 } from './base64images.js';
import ratatouilleSign from './assets/ratatouille_sign.png';

const data = [
  {
    question: "What's up Remy, what can I make with this stuff?",
    answer: "You can make a refreshing and spicy smashed cucumber salad with a tangy dressing!",
    image: remyBase64,
  },
  {
    question: "What's up Remy, I'm done cutting.",
    answer: "Great! Now mix 1 teaspoon salt, 2 teaspoons sugar, 1 teaspoon sesame oil, 2 teaspoons soy sauce, and 1 tablespoon rice vinegar to make the dressing.",
    image: remyBase64,
  },
  {
    question: "What's up, Remy? Dressing is ready. What now?",
    answer: "Toss the cucumber with the dressing, 3 chopped garlic cloves, and 1 teaspoon chili oil.",
    image: remyBase64,
  },
  {
    question: "What's up, Remy? I've mixed everything. How do I finish it?",
    answer: "Garnish the cucumber with 1 teaspoon sesame seeds and some chopped cilantro. Enjoy your smashed cucumber salad!",
    image: remyBase64,
  },
  {
    question: "What's up Remy, what can I make with this stuff?",
    answer: "You can make a refreshing and spicy smashed cucumber salad with a tangy dressing!",
    image: remyBase64,
  },
  {
    question: "What's up Remy, I'm done cutting.",
    answer: "Great! Now mix 1 teaspoon salt, 2 teaspoons sugar, 1 teaspoon sesame oil, 2 teaspoons soy sauce, and 1 tablespoon rice vinegar to make the dressing.",
    image: remyBase64,
  },
  {
    question: "What's up, Remy? Dressing is ready. What now?",
    answer: "Toss the cucumber with the dressing, 3 chopped garlic cloves, and 1 teaspoon chili oil.",
    image: remyBase64,
  },
  {
    question: "What's up, Remy? I've mixed everything. How do I finish it?",
    answer: "Garnish the cucumber with 1 teaspoon sesame seeds and some chopped cilantro. Enjoy your smashed cucumber salad!",
    image: remyBase64,
  },
];

function App() {
  return (
    <div className="app-wrapper">
      <div className="sign-container">
        <img src={ratatouilleSign} alt="Ratatouille Sign" className="ratatouille-sign" />
      </div>
      <div className="container">
        {data.map((item, index) => (
          <div className="card" key={index}>
            <img src={item.image} alt={`Image for ${item.question}`} />
            <div className="card-content">
              <h3>{item.question}</h3>
              <p>{item.answer}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
