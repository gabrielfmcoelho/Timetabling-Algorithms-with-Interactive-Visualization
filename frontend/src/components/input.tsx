import { Braces } from "lucide-react"
import { Button } from "./ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "./ui/dialog"

import { JsonEditor } from 'json-edit-react'

import jsonData from '../../data/mock/input.json'
import { ScrollArea } from "./ui/scroll-area"

export function Input() {
    return (
        <Dialog>
            <DialogTrigger>
              <Button
                variant={'secondary'} 
                className="text-muted-foreground hover:text-slate-900
                flex items-center gap-2"
              >
                <Braces size={15} />
                Dados de Entrada
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Dados de Entrada</DialogTitle>
                <DialogDescription>
                  Adicione ou altere os dados de entrada para a execuçãos dos algoritmos de timetabling
                </DialogDescription>
              </DialogHeader>
              <ScrollArea className="h-[400px] w-full">
                <JsonEditor
                  data={jsonData}
                  collapse={false}
                />
              </ScrollArea>
            </DialogContent>
          </Dialog>
    )
}