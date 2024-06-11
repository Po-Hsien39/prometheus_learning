import { useState, useEffect } from "react";
import TodoItem from "./todo_item";

function Section(props){
    const [todoItem, setTodoItem] = useState([])
    const [input, setInput] = useState('')
    const [todoNum, setTodoNum] = useState(0)
    const [update, setUpdate] = useState(true)
    const deleteNum = (num) => {
        setTodoItem(todoItem.map(item=>{
            if (item.num === num)
                item.delete = !item.focus
            return item
    }))}

    const editChecked = (num)=>{
        setTodoItem(todoItem.map(item=>{
            if (item.num === num)
                item.focus = !item.focus
            return item
        }))
        setUpdate(!update)
    }
    // Update how many tasks are left
    useEffect(()=>{
        let num = 0;
        let rest = 0
        todoItem.map((item)=>{
            if (item.focus === false && item.delete === false)
                num += 1;
            if (!item.delete)
                rest += 1;
        })
        props.editNum(num)
        if (rest === 0){
            props.displayTask(false)
        }else{
            props.displayTask(true)
        }
    }, [todoItem])

    // Setting mode
    useEffect(()=>{
        if (props.mode === 'all'){
            setTodoItem(todoItem.map((item)=>{
                item.hide = false;
                return item
            }))
        }else if (props.mode === 'active'){
            setTodoItem(todoItem.map((item)=>{
                (item.focus)?item.hide=true:item.hide=false
                return item
            }))
        }else if (props.mode === 'delete'){
            setTodoItem(todoItem.map((item)=>{
                (item.focus)?item.delete=true:item.delete=item.delete
                return item
            }))
        }else{
            setTodoItem(todoItem.map((item)=>{
                (!item.focus)?item.hide=true:item.hide=false
                return item
            }))
        }
    }, [props.mode, update])

    const appendNewTodo = (e)=>{
        if (e.key === "Enter"){
            setTodoItem((oldArr)=>[...oldArr, {num: todoNum, value: input, focus: false, delete: false, hide: false}])
            setTodoNum(todoNum + 1)
            setInput('')
        }
    }

    return (
        <section className="todo-app__main">
            <input value={input} onInput={e => setInput(e.target.value)} className="todo-app__input" placeholder="What needs to be done?" onKeyUp={appendNewTodo}/>
            <ul className="todo-app__list" id="todo-list">
                {todoItem.map((item)=>{
                    return (<TodoItem key={item.num} 
                        length={item.num} 
                        value={item.value} 
                        deleteNum={deleteNum} 
                        modify={editChecked}
                        status={item.hide || item.delete}/>)
                })}
            </ul>
        </section>
    )
}

export default Section;