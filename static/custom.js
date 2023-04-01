$(document).ready(function(){
	var _vm=$(this);
	var _index=_vm.attr('data-index');
	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});

	// change currency
	$(".choose-currency").on('click',function(){
		var _selected_currency=$(this).attr('data-currency');

		// Ajax
		$.ajax({
			url:'/change-currency',
			data:{
				'id':_selected_currency
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				_vm.attr('disabled',false);
			}
		});
		// End 
		
		$(document).ajaxStop(function(){
			window.location.reload();
		});

	});
	// End

	// Product Variation
	$(".choose-size").hide();
	$(".choose-image").hide();


	// Show size according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-size").removeClass('active');
		$(".choose-color").removeClass('focused');
		$(".tab-pane").removeClass('active')
		$(this).addClass('focused');

		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".choose-image").hide();
		$(".color"+_color).show();
		$(".image"+_color).show();
		$(".image"+_color).parent().first().addClass('active');
		//$(".color"+_color).first().addClass('active');

		var _price=$(".color"+_color).first().attr('data-price-'+selected_product);
		var _discount=$(".color"+_color).first().attr('data-discount-'+selected_product);
		var _discountlabel=$(".color"+_color).first().attr('data-discountlabel-'+selected_product);
		var _stock=$(".color"+_color).first().attr('data-stock-'+selected_product);
		var _image = "/media/" + $(".image"+_color+selected_product).first().attr('data-image-'+selected_product);;
		$(".product-image-"+selected_product).attr('src',_image);
		$(".product-discount-"+selected_product).text(_discount);
		$(".product-discount-label-"+selected_product).text(_discountlabel);
		$(".product-price-"+selected_product).text(_price);
		$(".product-stock-"+selected_product).text(_stock);
		$(".product-home-image-"+selected_product).css("background-image","url(" + _image + ")");

	});
	// End

	// Show the price according to selected size
	$(".choose-size").on('click',function(){
		$(".choose-size").removeClass('active');
		$(this).addClass('active');

		var _price=$(this).attr('data-price-'+selected_product);
		var _discount=$(this).attr('data-discount-'+selected_product);
		var _discountlabel=$(this).attr('data-discountlabel-'+selected_product);
		var _stock=$(this).attr('data-stock-'+selected_product);
		$(".product-discount-"+selected_product).text(_discount);
		$(".product-discount-label-"+selected_product).text(_discountlabel);
		$(".product-stock-"+selected_product).text(_stock);
		$(".product-price-"+selected_product).text(_price);
	})
	// End

	// Show the first selected color
	// $(".choose-color").first().addClass('focused');
	var _color=$(".choose-color").first().attr('data-color');
	var _price=$(".choose-size").first().attr('data-price-'+selected_product);
	var _discount=$(".choose-size").first().attr('data-discount-'+selected_product);
	var _discountlabel=$(".choose-size").first().attr('data-discountlabel-'+selected_product);
	var _stock=$(".color"+_color).first().attr('data-stock-'+selected_product);

	$(".image"+_color).show();
	$(".color"+_color).show();
	// $(".tab-pane").first().addClass('active');
	// $(".color"+_color).first().addClass('active');
	$(".product-discount-"+selected_product).text(_discount);
	$(".product-discount-label-"+selected_product).text(_discountlabel);
	$(".product-price-"+selected_product).text(_price);
	$(".product-stock-"+selected_product).text(_stock);

	var selected_color=0;
	var selected_size=0;
	var selected_product = 0;

	// get product id
	$(document).on('mouseover',".get_product_id",function(){
		selected_product = $(this).attr('data-productid')
	});

	// select color
	$(document).on('click',".choose-color",function(){
		selected_color=$(this).attr('data-color');
	});

	// select size
	$(document).on('click',".choose-size",function(){
		selected_size=$(this).attr('data-size');
	});

	// set all to 0
	$(document).on('mouseleave',".get_product_id",function(){
		selected_color=0;
		selected_size=0;
		selected_product = 0;
	});

	// Add to cart
	$(document).on('click',".add-to-cart",function(){
		if(selected_color == 0 || selected_size == 0){
			alert("Please select color and size")
		} else{
			var _vm=$(this);
			var _index=_vm.attr('data-index');
			var _qty=$(".product-qty-"+_index).val();
			var _selectedColor=selected_color;
			var _selectedSize=selected_size;
			var _productId=$(".product-id-"+_index).val();
			var _productImage=$(".product-image-"+_index).val();
			var _productTitle=$(".product-title-"+_index).val();
			var _productPrice=$(".product-discount-"+_index).text();
			// Ajax
			$.ajax({
				url:'/add-to-cart',
				data:{
					'id':_productId,
					'image':_productImage,
					'qty':_qty,
					'color':_selectedColor,
					'size':_selectedSize,
					'title':_productTitle,
					'price':_productPrice
				},
				dataType:'json',
				beforeSend:function(){
					_vm.attr('disabled',true);
				},
				success:function(res){
					$(".cart-list").text(res.totalitems);
					_vm.attr('disabled',false);
				}
			});
			// End
			$(document).ajaxStop(function(){
				window.location.reload();
			});
		}
	});
	// End

	// Add to cart attribute
	$(document).on('click',".add-to-cart-attribute",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _qty=$(".product-qty-"+_index).val();
		var _productId=$(".product-id-"+_index).val();
		// Ajax
		$.ajax({
			url:'/add-to-cart-attribute',
			data:{
				'id':_productId,
				'qty':_qty,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});
		// End
		$(document).ajaxStop(function(){
			window.location.reload();
		});
	});
	// End

	// Delete item from cart
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
		
		// EndAjax
		$(document).ajaxStop(function(){
			window.location.reload();
		});
	});

	// Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

	// Add wishlist
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/add-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');
				}
			}
		});
		// EndAjax
		$(document).ajaxStop(function(){
			window.location.reload();
		});
	});
	// End

	// Delete wishlist
	$(document).on('click',".delete-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/delete-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
			}
		});
		// EndAjax
		$(document).ajaxStop(function(){
			window.location.reload();
		});
	});
	// End

	// Activate selected address
	$(document).on('click','.activate-address',function(){
		var _aId=$(this).attr('data-address');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/activate-address',
			data:{
				'id':_aId,
			},
			dataType:'json',
			success:function(res){
				$(".address-cost").load(location.href + " .address-cost");
				if(res.bool==true){
					$(".address").removeClass('shadow border-secondary');
					$(".address"+_aId).addClass('shadow border-secondary');

					$(".check").hide();
					$(".actbtn").show();
					
					$(".check"+_aId).show();
					$(".btn"+_aId).hide();
				}
			}
		});
		// End
	});

});
// End Document.Ready

// Product Review Save
$("#addForm").submit(function(e){
	$.ajax({
		data:$(this).serialize(),
		method:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType:'json',
		success:function(res){
			if(res.bool==true){
				$(".ajaxRes").html('Data has been added.');
				$("#reset").trigger('click');
				// Hide Button
				$(".reviewBtn").hide();
				// End

				// create data for review
				var _html='<blockquote class="blockquote text-right">';
				_html+='<small>'+res.data.review_text+'</small>';
				_html+='<footer class="blockquote-footer">'+res.data.user;
				_html+='<cite title="Source Title">';
				for(var i=1; i<=res.data.review_rating; i++){
					_html+='<i class="fa fa-star text-warning"></i>';
				}
				_html+='</cite>';
				_html+='</footer>';
				_html+='</blockquote>';
				_html+='</hr>';

				$(".no-data").hide();

				// Prepend Data
				$(".review-list").prepend(_html);

				// Hide Modal
				$("#productReview").modal('hide');

				// AVg Rating
				$(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
			}
		}
	});
	e.preventDefault();
});
// End

// delete Review
$(document).on('click',".delete-review",function(){
	var _pid=$(this).attr('data-review');
	var _vm=$(this);
	// Ajax
	$.ajax({
		url:"/delete-review",
		data:{
			review:_pid
		},
		dataType:'json',
		success:function(res){
		}
	});
	// EndAjax
	$(document).ajaxStop(function(){
		window.location.reload();
	});
});
// End