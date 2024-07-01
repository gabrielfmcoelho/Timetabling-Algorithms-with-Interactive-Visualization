import { 
    Calendar, 
    Play 
} from "lucide-react";

import { 
    Card, 
    CardHeader 
} from "./ui/card";

import { Button } from "./ui/button";

import { 
    Select, 
    SelectTrigger, 
    SelectValue,
    SelectContent, 
    SelectItem 
} from "./ui/select";

export function Header() {
    return (
        <Card className="w-screen">
            <CardHeader className="flex flex-row items-center justify-between">
                <h1 className="font-bold text-xl flex items-center gap-2">
                    <Calendar size={20} strokeWidth={2.85} />
                    TimeTabling
                </h1>
                <div className="flex items-center gap-2">
                    <Select>
                        <SelectTrigger className="w-[300px]">
                            <SelectValue placeholder="Selecione o algoritmo" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem 
                                value="genetic-algorithms" 
                                className="cursor-pointer"
                            >
                                Algoritmo Genético 
                            </SelectItem>
                            <SelectItem 
                                value="local-search" 
                                className="cursor-pointer"
                            >
                                Algoritmo de Busca Local
                            </SelectItem>
                        </SelectContent>
                    </Select>
                    <Button 
                        className="flex items-center gap-2"
                    >
                        <Play size={20} />
                        Run
                    </Button>
                </div>
            </CardHeader>
        </Card>
    )
}