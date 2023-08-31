import axios, { AxiosResponse } from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000'
});

export const upload = async (
    browsingHistory: File,
    likeHistory: File,
    favoriteHistory: File,
    commentHistory: File,
    searchHistory: File,
    shareHistory: File
): Promise<AxiosResponse<any>> => {
    const formData = new FormData();
    formData.append('browsing_history', browsingHistory);
    formData.append('like_history', likeHistory);
    formData.append('favorite_history', favoriteHistory);
    formData.append('comment_history', commentHistory);
    formData.append('search_history', searchHistory);
    formData.append('share_history', shareHistory);

    try {
        const response = await api.post('/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        console.log(response);
        return response;
    } catch (error) {
        console.error('An error occured while uploading data: ', error);
        throw error;
    }
};