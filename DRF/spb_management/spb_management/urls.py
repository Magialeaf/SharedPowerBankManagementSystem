"""
URL configuration for spb_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users import views as users_api
from areas import views as areas_api
from merchants import views as merchants_api
from system_administration import views as system_administration_api
from orders import views as orders_api
from power_bank import views as power_bank_api

urlpatterns = [
    # path('admin/', admin.site.urls),

    # users app
    path('<str:version>/enter/', users_api.EnterView.as_view(), name='enter_detail'),
    path('<str:version>/captcha/<str:pk>/', users_api.CaptchaView.as_view(), name='captcha_detail'),
    path('<str:version>/my-info/', users_api.MyInfoView.as_view(), name='my_info_detail'),
    path('<str:version>/one-info/<int:pk>/', users_api.OneInfoView.as_view(), name='one_info_detail'),
    path('<str:version>/user/<int:pk>/', users_api.UserView.as_view(), name='user_detail'),
    path('<str:version>/account/<int:pk>/', users_api.AccountView.as_view(), name='account_detail'),
    path('<str:version>/user/avatar/', users_api.UserAvatarView.as_view(), name='user_avatar_detail'),
    path('<str:version>/maintain/<int:pk>/', users_api.MaintainView.as_view(), name='maintain_detail'),

    # areas app
    path('<str:version>/area/<int:pk>/',  areas_api.AreaView.as_view(), name='area_detail'),

    # merchants app
    path('<str:version>/merchant/<int:pk>/', merchants_api.MerchantView.as_view(), name='merchant_detail'),
    path('<str:version>/merchant/img/', merchants_api.MerchantImgView.as_view(), name='merchant_img_detail'),
    path('<str:version>/hot-merchant/', merchants_api.HotMerchantView.as_view(), name='hot_merchant_detail'),

    # power_bank app
    path('<str:version>/power-bank/<int:pk>/', power_bank_api.PowerBankView.as_view(), name='power_bank_detail'),
    path('<str:version>/power-bank/img/', power_bank_api.PowerBankImgView.as_view(), name='power_bank_img_detail'),
    path('<str:version>/power-bank/maintenance/<int:pk>/', power_bank_api.PowerBankMaintenanceView.as_view(), name='power_bank_maintenance_detail'),
    path('<str:version>/hot-power-bank/', power_bank_api.HotPowerBankView.as_view(), name='hot_power_bank_detail'),

    # orders app
    path('<str:version>/power-bank-fee/<int:pk>/', orders_api.PowerBankFeeView.as_view(), name='power_bank_fee_detail'),
    path('<str:version>/power-bank-rental/<int:pk>/', orders_api.PowerBankRentalView.as_view(), name='power_bank_rental_detail'),
    path('<str:version>/power-bank-return/<int:pk>/', orders_api.PowerBankReturnView.as_view(), name="power_bank_return_detail"),
    path('<str:version>/user-order-operation/<int:pk>/', orders_api.UserOrderOperationView.as_view(), name='user_order_operation_detail'),


    # system_administration app
    path('<str:version>/system-administration/carousel-chart/<int:pk>/', system_administration_api.CarouselChartView.as_view(), name='carousel_chart_detail'),
    path('<str:version>/system-administration/carousel-chart/img/', system_administration_api.CarouselChartImgView.as_view(), name='carousel_chart_img_detail'),
    path('<str:version>/system-administration/notice/<int:pk>/', system_administration_api.NoticeView.as_view(), name="notice_detail"),
    path('<str:version>/system-administration/notice/img/', system_administration_api.NoticeImgView.as_view(), name='notice_img_detail'),
]

# 主路由中：显性告诉django绑定media_url和media_root
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 然后在app分布式路由中：添加对应的视图函数(一般用户上传的文件单独写在一个视图函数中)
