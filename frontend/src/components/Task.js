const Task = ({task}) => {
    return (
        <div>
            <p>{task.title}</p>
            <p>{task.completed ? 'Completed' : 'In progress'}</p>
        </div>
    )
}

export default Task;