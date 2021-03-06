from django.shortcuts import render,HttpResponse, get_object_or_404
from .models import Sector,PrecioEmpresa,Empresa
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

# Create your views here.

def index(request):
    #sector = Sector.objects.all()
    return render (request,"empresas/index.html",{"sectores":Sector.objects.all()})

def sector(request,id):
    sector = get_object_or_404(Sector, pk=id)
    return render (request,"empresas/sector.html",{"sector":sector})

def precio_empresas(request,id):
    precio_empresa = get_object_or_404(PrecioEmpresa, pk=id)
    return render (request,"empresas/precio_empresas.html",{"precio_empresa":precio_empresa})

def empresa(request,id):
    empresa = Empresa.objects.get(pk=id)
    precios_empresa = empresa.precioempresa_set.all()
    return render(request,"empresas/empresa.html",{"precios_empresa":precios_empresa,"empresa":empresa})


class LineChartJSONView(BaseLineChartView):
    
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        #return ("January", "February", "March", "April", "May", "June", "July")
        empresa = Empresa.objects.get(pk=1)
        precios_empresa = empresa.precioempresa_set.all()

        fechas = []
        for precio_empresa in precios_empresa:
            fechas.append(precio_empresa.fecha)

        return fechas


    def get_providers(self):
        """Return names of datasets."""
        return ["Central"]

    def get_data(self):
        
        empresa = Empresa.objects.get(pk=1)
        precios_empresa = empresa.precioempresa_set.all()

        precioCierre = []
        for precio_empresa in precios_empresa:
            precioCierre.append(precio_empresa.precio_cierre)


        return [precioCierre]

        #return [[75, 44, 92, 11, 44, 95, 35],
         #       [41, 92, 18, 3, 73, 87, 92],
          #      [87, 21, 94, 3, 90, 13, 65]]

line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()