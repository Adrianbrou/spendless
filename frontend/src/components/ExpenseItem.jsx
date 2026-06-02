// This component draws ONE expense row. That's its only job.
// It owns no data - it just receives one `expense` (a prop) and displays it.
function ExpenseItem({ expense }) {
    return (
        <li>
            {expense.description}: ${expense.amount_cents / 100}
        </li>
    );
}

export default ExpenseItem;
