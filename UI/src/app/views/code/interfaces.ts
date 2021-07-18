export interface Snippet {
    id: string;
    name: string;
    code: string;
    language: string;
    revision: Date;
}

export interface ExecutionResult {
    res: string;
    error: string;
}