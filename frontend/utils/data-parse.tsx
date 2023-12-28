interface VideoRecord {
    date: Date;
    id: string;
}

interface CommentRecord {
    date: Date;
    comment: string;
}

interface SearchRecord {
    date: Date;
    search: string;
}

interface ShareRecord {
    date: Date;
    type: string;
    id: string;
    method: string;
}

/**
 * Reads the content of a file.
 * 
 * @param file - The file to be read.
 * @returns A promise that resolves with the content of the file as a string.
 */
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

/**
 * Extracts date and video ID from txt file.
 * Works for browsing history, liked, and favorites.
 * 
 * @param content - The content of the file as a string.
 * @returns An array of VideoRecord objects, each containing a date and an ID.
 */
export const parseDateId = (content: string): VideoRecord[] => {
    const lines = content.trim().split('\n');
    const videos: VideoRecord[] = [];
    let curr: Partial<VideoRecord> = {};

    lines.forEach(line => {
        if (line.startsWith("Date:")) {
            curr.date = new Date(line.substring("Date: ".length));
        } else if (line.startsWith("Link:")) {
            curr.id = getIdFromLine(line);
        } else if (line === "" && curr.date && curr.id) {
            videos.push(curr as VideoRecord);
            curr = {};
        }
    });
    return videos;
};

/**
 * Extracts date and comment from txt file.
 * Works for comment history only.
 * 
 * @param content - The content of the file as a string.
 * @returns An array of CommentRecord objects, each containing a date and a comment.
 */
export const parseComments = (content: string): CommentRecord[] => {
    const lines = content.trim().split('\n');
    const comments: CommentRecord[] = [];
    let curr: Partial<CommentRecord> = {};

    lines.forEach(line => {
        if (line.startsWith("Date:")) {
            curr.date = new Date(line.substring("Date: ".length));
        } else if (line.startsWith("Comment:")) {
            curr.comment = line.substring("Comment: ".length);
        } else if (line === "" && curr.date && curr.comment) {
            comments.push(curr as CommentRecord);
            curr = {};
        }
    });
    return comments;
};

/**
 * Extracts date and search terms from txt file.
 * Works for search history only.
 * 
 * @param content - The content of the file as a string.
 * @returns An array of SearchRecord objects, each containing a date and a search term.
 */
export const parseSearches = (content: string): SearchRecord[] => {
    const lines = content.trim().split('\n');
    const searches: SearchRecord[] = [];
    let curr: Partial<SearchRecord> = {};

    lines.forEach(line => {
        if (line.startsWith("Date:")) {
            curr.date = new Date(line.substring("Date: ".length));
        } else if (line.startsWith("Search Term:")) {
            curr.search = line.substring("Search Term: ".length);
        } else if (line === "" && curr.date && curr.search) {
            searches.push(curr as SearchRecord);
            curr = {};
        }
    });
    return searches;
};

/**
 * Extracts date, content type, id, and method from txt file.
 * Works for share history only.
 * 
 * @param content - The content of the file as a string.
 * @returns An array of ShareRecord objects, each containing a date, type, id, and method.
 */
export const parseShares = (content: string): ShareRecord[] => {
    const lines = content.trim().split('\n');
    const shares: ShareRecord[] = [];
    let curr: Partial<ShareRecord> = {};

    lines.forEach(line => {
        if (line.startsWith("Date:")) {
            curr.date = new Date(line.substring("Date: ".length));
        } else if (line.startsWith("Shared Content:")) {
            curr.type = line.substring("Shared Content: ".length);
        } else if (line.startsWith("Link:")) {
            curr.id = getIdFromLine(line);
        } else if (line.startsWith("Method:")) {
            curr.method = line.substring("Method: ".length);
        } else if (line === "" && curr.date && curr.type && curr.id && curr.method) {
            shares.push(curr as ShareRecord);
            curr = {};
        }
    });
    return shares;
};

/**
 * Extracts the ID from a line containing a URL.
 * 
 * @param line - A string line containing a URL.
 * @returns The extracted ID from the URL.
 */
const getIdFromLine = (line: string): string => {
    return line.split("/").slice(-2)[0].trim();
};
