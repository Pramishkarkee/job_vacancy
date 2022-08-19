const countryProvider = document.getElementById('id_address-0-country');
const provinceProvider = document.getElementById('id_address-0-province');
const districtProvider = document.getElementById('id_address-0-district');
const vdcProvider = document.getElementById('id_address-0-vdc_municipality');
const wardNoProvider = document.getElementById('id_address-0-ward_number');

const provinceDefaultOptionText = '(Select Province)';
const districtDefaultOptionText = '(Select District)';
const vdcDefaultOptionText = '(Select VDC/Municipality)';
const wardNoDefaultOptionText = '(Select Ward Number)';

Element.prototype.remove = function () {
  this.parentElement.removeChild(this);
};

HTMLSelectElement.prototype.addOption = function (optionValue, optionText) {
  const node = document.createElement('option');
  node.value = optionValue;
  node.innerText = optionText;
  this.appendChild(node);
};

HTMLSelectElement.prototype.assignChildNodes = function (rootChildNodes) {
  for (var i = 0; i < rootChildNodes.length; i++) {
    let tempNode = rootChildNodes[i].cloneNode(true);
    this.appendChild(tempNode);
  }
};

NodeList.prototype.remove = HTMLCollection.prototype.remove = function () {
  while (this[0]) {
    this[0].remove();
  }
};

HTMLSelectElement.prototype.copy = function (rootElement) {
  this.childNodes.remove();
  this.assignChildNodes(rootElement.childNodes);
  this.value = rootElement.value;
};

NodeList.prototype.removeExcept = function (optiontext) {
  while (this[0]) {
    if (this[0].text != optiontext) {
      this[0].remove();
    } else if (this[1]) {
      this[1].remove();
    } else {
      break;
    }
  }
};

updateProvince = function () {
  provinceProvider.childNodes.removeExcept(provinceDefaultOptionText);
  districtProvider.childNodes.removeExcept(districtDefaultOptionText);
  vdcProvider.childNodes.removeExcept(vdcDefaultOptionText);
  wardNoProvider.childNodes.removeExcept(wardNoDefaultOptionText);

  var provinceSelect = provinceProvider;
  var country = countryProvider.value;

  if (!country) return;
  return fetch(`/getProvince/${country}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        provinceSelect.addOption(el[0], el[1]);
      });
      updateDistrict();
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

updateDistrict = function () {
  districtProvider.childNodes.removeExcept(districtDefaultOptionText);
  vdcProvider.childNodes.removeExcept(vdcDefaultOptionText);
  wardNoProvider.childNodes.removeExcept(wardNoDefaultOptionText);

  var districtSelect = districtProvider;
  var province = provinceProvider.value;

  if (!province) return;
  return fetch(`/getDistrict/${province}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        districtSelect.addOption(el[0], el[1]);
      });
      updateVDCMunicipality();
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

updateVDCMunicipality = function () {
  vdcProvider.childNodes.removeExcept(vdcDefaultOptionText);
  wardNoProvider.childNodes.removeExcept(wardNoDefaultOptionText);

  var vdcMunicipalitySelect = vdcProvider;
  var district = districtProvider.value;

  if (!district) return;
  return fetch(`/getVDCMunicipality/${district}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        vdcMunicipalitySelect.addOption(el[0], el[1]);
      });
      updateWardNumber();
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

updateWardNumber = function () {
  wardNoProvider.childNodes.removeExcept(wardNoDefaultOptionText);

  var wardNoSelect = wardNoProvider;
  var vdcMunicipality = vdcProvider.value;

  if (!vdcMunicipality) return;
  return fetch(`/getWardNumber/${vdcMunicipality}`)
    .then((res) => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    })
    .then((data) => {
      data.forEach((el) => {
        wardNoSelect.addOption(el[0], el[1]);
      });
    })
    .catch((err) => {
      console.error(
        'There has been a problem with your fetch operation: ',
        err.message
      );
    });
};

async function setAddressInitial() {
  await updateProvince();

  if (countryValue) {
    countryProvider.selectedIndex = [...countryProvider.options].findIndex(
      (option) => option.text === countryValue
    );

    await updateProvince();
    provinceProvider.selectedIndex = [...provinceProvider.options].findIndex(
      (option) => option.text === provinceValue
    );

    await updateDistrict();
    districtProvider.selectedIndex = [...districtProvider.options].findIndex(
      (option) => option.text === districtValue
    );

    await updateVDCMunicipality();
    vdcProvider.selectedIndex = [...vdcProvider.options].findIndex(
      (option) => option.text === vdcValue
    );

    await updateWardNumber();
    wardNoProvider.selectedIndex = [...wardNoProvider.options].findIndex(
      (option) => option.text === wardNoValue
    );
  }
}

window.addEventListener('load', async (event) => {
  setAddressInitial();
});

countryProvider.addEventListener('change', (event) => {
  updateProvince();
});
provinceProvider.addEventListener('change', (event) => {
  updateDistrict();
});
districtProvider.addEventListener('change', (event) => {
  updateVDCMunicipality();
});
vdcProvider.addEventListener('change', (event) => {
  updateWardNumber();
});
