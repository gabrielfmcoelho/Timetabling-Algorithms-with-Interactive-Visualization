import { Calendar, Play } from "lucide-react";
import { Card, CardContent, CardHeader } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Tabs, TabsList, TabsTrigger } from "./components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Table, TableHeader, TableRow, TableHead, TableCell, TableBody } from "./components/ui/table";

export function App() {
  return (
    <main className="flex flex-col items-center gap-10">
      <Card className="w-screen">
        <CardHeader className="flex flex-row items-center justify-between">
          <h1 className="font-bold text-xl flex items-center gap-2">
            <Calendar size={20} strokeWidth={2.85} />
            TimeTabling
          </h1>
          <div className="flex items-center gap-2">
            <Select>
              <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Selecione o modelo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="genetic-algorithms" className="cursor-pointer">
                  Algoritmo Genético 
                </SelectItem>
                <SelectItem value="neural-networks" className="cursor-pointer">
                  Rede Neural
                </SelectItem>
              </SelectContent>
            </Select>
            <Button className="flex items-center gap-2">
              <Play size={20} />
              Run
            </Button>
          </div>
        </CardHeader>
      </Card>
      <Card className="w-[1000px]">
        <CardHeader className="flex flex-row items-center justify-between">
          <Tabs defaultValue="segunda">
            <TabsList>
              <TabsTrigger value="segunda">Segunda</TabsTrigger>
              <TabsTrigger value="terca">Terça</TabsTrigger>
              <TabsTrigger value="quarta">Quarta</TabsTrigger>
              <TabsTrigger value="quinta">Quinta</TabsTrigger>
              <TabsTrigger value="sexta">Sexta</TabsTrigger>
            </TabsList>
          </Tabs>
          <Select>
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Selecione a turma" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="alpha">Alpha</SelectItem>
              <SelectItem value="zeta">Zeta</SelectItem>
              <SelectItem value="shaw">Shaw</SelectItem>
            </SelectContent>
          </Select>
        </CardHeader>
        <CardContent>
        <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="text-left">Sala</TableHead>
                <TableHead className="text-center">Matéria</TableHead>
                <TableHead className="text-center">Professor(a)</TableHead>
                <TableHead className="text-right">Horário</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell className="text-left">Sala 10</TableCell>
                <TableCell className="text-center">Inteligencia Artifical</TableCell>
                <TableCell className="text-center">Dimmy Magalhães</TableCell>
                <TableCell className="text-right">18:30 - 20:30</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="text-left">Sala 10</TableCell>
                <TableCell className="text-center">Inteligencia Artifical</TableCell>
                <TableCell className="text-center">Dimmy Magalhães</TableCell>
                <TableCell className="text-right">18:30 - 20:30</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="text-left">Sala 10</TableCell>
                <TableCell className="text-center">Inteligencia Artifical</TableCell>
                <TableCell className="text-center">Dimmy Magalhães</TableCell>
                <TableCell className="text-right">18:30 - 20:30</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </main>
  )
}