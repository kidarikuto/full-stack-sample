'use client'
import axios from 'axios'
import React, { useEffect, useState } from 'react'

export default function Page(){
    const [data, setData]=useState({ message:''})

    useEffect(()=>{
        axios.get('http://127.0.0.1:8000/api/hello/backend/')
        .then((res)=>res.data)
        .then((data)=>{
            setData(data)
        })
        .catch((error) => {
            console.error('API request failed:', error);
        });

        // .then((res) => {
        //     console.log('Response data:', res.data); // レスポンスデータをコンソールに表示
        //     return res.data;
        //   })
        //   .then((data) => {
        //     setData(data);
        //   })
        //   .catch((error) => {
        //     console.error('API request failed:', error);
        //   });
    },[])

    return <div>hello {data.message}!</div>
}