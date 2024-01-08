export const parseFile = (file: File) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = (event) => {
            resolve(event.target!.result);
        };
        reader.onerror = (error) => {
            reject(error);
        };
    });
};

export const processDataForD3 = (data: any) => {
    const parsedData = JSON.parse(data);
    const formattedData = parsedData.map((d: any) => {
        const obj: any = {};
        obj["date"] = new Date(d.timestampMs);
        obj["value"] = d.value;
        return obj;
    });
    return formattedData;
}