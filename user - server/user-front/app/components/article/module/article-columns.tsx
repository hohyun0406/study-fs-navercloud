import { Link, Typography } from "@mui/material";
import { ArticleColumn } from "../model/article-column";
import { GridColDef } from "@mui/x-data-grid";
import { PG } from "../../common/enums/PG";

interface CellType{
    row : ArticleColumn
}

export default function ArticleColumns() : GridColDef[]{
    return [
        {
            flex: 0.04,
            minWidth : 30,
            sortable : false,
            field: 'id',
            headerName : 'No.',
            renderCell: ({row} : CellType) => <Typography textAlign="center" sx={{fontSize:"1.5rem"}}>{row.id}</Typography>
        },
        {
            flex: 0.04,
            minWidth : 30,
            sortable : false,
            field: 'title',
            headerName : '제목',
            renderCell: ({row} : CellType) => <Typography textAlign="center" sx={{fontSize:"1.5rem"}}><Link href={`${PG.ARTICLE}/detail/${row.id}`}>{row.title}</Link></Typography>
        },
        {
            flex: 0.04,
            minWidth : 30,
            sortable : false,
            field: 'content',
            headerName : '내용',
            renderCell: ({row} : CellType) => <Typography textAlign="center" sx={{fontSize:"1.5rem"}}>{row.content}</Typography>
        },
        {
            flex: 0.04,
            minWidth : 30,
            sortable : false,
            field: 'registerDate',
            headerName : '등록일',
            renderCell: ({row} : CellType) => <Typography textAlign="center" sx={{fontSize:"1.5rem"}}>{row.registerDate}</Typography>
        },
        {
            flex: 0.04,
            minWidth : 30,
            sortable : false,
            field: 'wrtierId',
            headerName : '작성자아이디',
            renderCell: ({row} : CellType) => <Typography textAlign="center" sx={{fontSize:"1.5rem"}}>{row.wrtierId}</Typography>
        },
        {
            flex: 0.04,
            minWidth : 30,
            sortable : false,
            field: 'boardId',
            headerName : '보드아이디',
            renderCell: ({row} : CellType) => <Typography textAlign="center" sx={{fontSize:"1.5rem"}}>{row.boardId}</Typography>
        },
        {
            flex: 0.04,
            minWidth: 30,
            sortable: false,
            field: 'delete',
            headerName: '삭제',
            renderCell: ({row}:CellType) => <Link href={""}>  {<Typography textAlign="center" sx={{fontSize:"1.5rem"}}> 삭제 </Typography>}</Link>
            },
    ]
}