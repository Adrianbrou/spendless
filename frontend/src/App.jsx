import ExpenseItem from "./components/ExpenseItem";
import { useState, useEffect } from "react";

function App() {

  const [expenses, setExpenses] = useState([])
  useEffect(() => {
    fetch("http://127.0.0.1:8000/expenses/?user_id=1")
      .then((res) => res.json())
      .then((data) => setExpenses(data))
  }, []);

  return (
    <div>
      <h1>Spendless</h1>
      <p>Hello from React</p>

      <h2>Expenses</h2>
      <ul>
        {expenses.map((expense) => (
          <ExpenseItem key={expense.id} expense={expense} />
        ))}
      </ul>
    </div>
  );
}

export default App;
