import type { NextApiResponse } from 'next'
type Data = {
    name: string
}

export default function handler(
    req:NextApiResponse,
    res:NextApiresponse<Data>
){
    res.status(200).json({ name:'Json Doe' })
}
