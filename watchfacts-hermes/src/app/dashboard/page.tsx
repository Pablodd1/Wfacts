import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Dashboard() {
  return (
    <div className="flex flex-col gap-4 p-8">
      <h1 className="text-3xl font-serif text-[#d4af37]">Platform Metrics</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground font-sans">Total Listings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12,345</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground font-sans">Exception Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">14.2%</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground font-sans">Auto-Clear Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">82.1%</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground font-sans">Backlog Queue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">164,000</div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
