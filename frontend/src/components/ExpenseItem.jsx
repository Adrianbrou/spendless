function ExpenseItem({ expense }) {
    return (
        <li>
            {expense.description}: ${expense.amount_cents / 100}
        </li>
    );
}

export default ExpenseItem;
