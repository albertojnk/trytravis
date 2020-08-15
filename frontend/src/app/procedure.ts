export interface Procedure {
    id: string;
    consultado: string;
    extraido: string;
    comarca: string;
    o_julgador: string;
    procedimento: string;
    ativa: string;
    passiva: string;
    e_ativa: string;
    e_passiva: string;
    created: string;
    progress: number;
}

export interface ProcedureProgress {
    procedures: Procedure[]
}