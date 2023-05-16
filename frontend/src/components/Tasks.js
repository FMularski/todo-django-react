import { useState, useEffect } from "react"
import axios from 'axios';
import Task from './Task';

const Tasks = () => {
    const [tasks, setTasks] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:8000/core/api/tasks/")
            .then(res => setTasks(res.data))
            .catch(err => console.log(err));
    }, [])

    return (
        <div>
            {tasks.map(task => <Task task={task} key={task.id} />)}
        </div>
    )
}

export default Tasks;