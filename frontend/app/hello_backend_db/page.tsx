'use client'
import axios from 'axios'
import React, {useEffect, useState} from 'react'

export default function Page(){
    const [data, setData] = useState({ message: ''})

    useEffect(()=>{
        axios.get('http://127.0.0.1:8000/api/hello_db/backend/')
        .then((res)=>res.data)
        .then((data)=>{
            setData(data)
        })
    }, [])

    return <div>hello{data.message}!</div>
}