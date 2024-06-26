import { 
  Card, 
  CardContent, 
  CardHeader 
} from "./components/ui/card";

import { Header } from "./components/header";

import { 
  Tabs, 
  TabsList, 
  TabsTrigger 
} from "./components/ui/tabs";

import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "./components/ui/select";

import { 
  Table, 
  TableHeader, 
  TableRow, 
  TableHead, 
  TableCell, 
  TableBody 
} from "./components/ui/table";

import { Input } from "./components/input";

export function App() {
  return (
    <main className="flex flex-col items-center gap-10">
      <Header />
      <Card className="w-[1000px]">
        <CardHeader className="flex flex-row items-center justify-between">
          <Input />
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