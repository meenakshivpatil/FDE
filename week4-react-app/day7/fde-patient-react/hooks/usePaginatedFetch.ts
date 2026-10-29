import { useState, useEffect } from "react"

export default function usePaginatedFetch(url: string, limit: number) {
    const [data, setData] = useState<any[]>([])
    const [offset, setOffset] = useState(0)

    useEffect(() => {
        fetch(`${url}?limit=${limit}&offset=${offset}`)
            .then(response => response.json())
            .then(fetchedData => setData(fetchedData))
    }, [url, limit, offset])

    return { data, offset, setOffset }
}